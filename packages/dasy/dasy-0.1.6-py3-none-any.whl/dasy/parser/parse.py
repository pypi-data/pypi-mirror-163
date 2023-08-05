import hy
import vyper.ast.nodes as vy_nodes
import vyper.compiler.phases as phases
from vyper.compiler.phases import CompilerData
from hy import models
from .utils import next_nodeid

BUILTIN_FUNCS = ['+', '-', '/', '*']

def parse_return(return_tree):
    val = return_tree[1]
    value_node = parse_node(val)
    return_node = vy_nodes.Return(value=value_node, ast_type='Return', node_id=next_nodeid())
    return return_node

def parse_binop(binop_tree):
    match str(binop_tree[0]):
        case '+' | '-' | '*' | '/':
            left = parse_node(binop_tree[1])
            right = parse_node(binop_tree[2])
            op = parse_node(binop_tree[0])
            return vy_nodes.BinOp(left=left, right=right, op=op, node_id=next_nodeid(), ast_type='BinOp')

def parse_args_list(args_list) -> [vy_nodes.arg]:
    if len(args_list) == 0:
        return []
    results = []
    current_type = args_list[0]
    assert isinstance(current_type, models.Keyword)
    # get annotation and name
    for arg in args_list[1:]:
        # get annotation and name
        annotation_node = vy_nodes.Name(id=str(current_type.name), parent=None, node_id=next_nodeid(), ast_type='Name')
        results.append(vy_nodes.arg(arg=str(arg), parent=None, annotation=annotation_node, node_id=next_nodeid()))
    return results

def parse_tuple(tuple_tree):
    match tuple_tree:
        case models.Symbol(q), elements if str(q) == 'quote':
            elts = [parse_node(e) for e in elements]
            return vy_nodes.Tuple(elements=elts, node_id=next_nodeid(), ast_type='Tuple')
        case _:
            raise Exception("Invalid tuple declaration; requires quoted list ex: '(2 3 4)")

def parse_fn(fn_tree):
    fn_node_id = next_nodeid()
    assert isinstance(fn_tree, models.Expression)
    assert fn_tree[0] == models.Symbol('defn')
    match fn_tree[1:]:
        case models.Symbol(sym_node), models.List(args_node), returns, models.Keyword(vis), *body:
            assert isinstance(returns, models.Keyword) or isinstance(returns, models.Expression)
            rets = parse_node(returns)
            name = str(sym_node)
            args_list = parse_args_list(args_node)
            args = vy_nodes.arguments(args=args_list, defaults=list(), node_id=next_nodeid(), ast_type='arguments')
            decorators = [vy_nodes.Name(id=vis, node_id=next_nodeid(), ast_type='Name')]
            fn_body = [parse_node(body_node) for body_node in body[:-1]]
            value_node = parse_node(body[-1])
            implicit_return_node = vy_nodes.Return(value=value_node, ast_type='Return', node_id=next_nodeid())
            fn_body.append(implicit_return_node)
        case _:
            raise Exception(f"Invalid fn form {fn_tree}")
    return vy_nodes.FunctionDef(args=args, returns=rets, decorator_list=decorators, pos=None, body=fn_body, name=name, node_id=fn_node_id, ast_type='FunctionDef')

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def parse_contract(expr):
    mod_node = vy_nodes.Module(body=[], name=str(expr[1]), doc_string="", ast_type='Module', node_id=next_nodeid())
    expr_body = []
    match expr[1:]:
        case (name, vars, *body) if isinstance(vars, models.List):
            # contract has state
            for var, typ in pairwise(vars):
                target = parse_node(var)
                is_constant = False
                is_public = False
                is_immutable = False
                match typ:
                    case [models.Symbol(e), models.Keyword(name)] if str(e) in ["public", "immutable", "constant"]:
                        annotation = parse_node(typ)
                        match str(e):
                            case "public":
                                is_public = True
                            case "immutable":
                                is_immutable = True
                            case "constant":
                                is_constant = True
                    case models.Keyword():
                        annotation = parse_node(typ)
                    case _:
                        raise Exception(f"Invalid declaration type {typ}")
                mod_node.add_to_body(vy_nodes.VariableDecl(ast_type='VariableDecl', node_id=next_nodeid(), target=target, annotation=annotation, value=None, is_constant=is_constant, is_public=is_public, is_immutable=is_immutable))
            expr_body = expr[3:]
        case (name, *body):
            # no contract state
            expr_body = expr[2:]
        case _:
            # print(f"no match: {expr}")
            raise Exception(f"Invalid defcontract form: {expr}")
    for node in expr_body:
        mod_node.add_to_body(parse_node(node))

    return mod_node

def parse_attribute(expr):
    match expr[1:]:
        case [obj, attr]:
            return vy_nodes.Attribute(ast_type='Attribute', node_id=next_nodeid(), attr=str(attr), value=parse_node(obj))

def parse_call(expr):
    match expr:
        case (fn_name, *args):
            args_list = [parse_node(arg) for arg in args]
            return vy_nodes.Call(func=parse_node(fn_name), args=args_list, keywords=[], ast_type='Call', node_id=next_nodeid())

def parse_assignment(expr):
    match expr[1:]:
        case [target, value]:
            return vy_nodes.Assign(ast_type='Call', node_id=next_nodeid(), targets=[parse_node(target)], value=parse_node(value))

def parse_expr(expr):
    match str(expr[0]):
        case "defcontract":
            return parse_contract(expr)
        case 'defn':
            return parse_fn(expr)
        case 'return':
            return parse_return(expr)
        case '+' | '-' | '*' | '/':
            node = parse_binop(expr)
            return node
        case 'quote':
            return parse_tuple(expr)
        case '.':
            return parse_attribute(expr)
        case 'setv':
            return parse_assignment(expr)
        case _:
            return parse_call(expr)

def parse_builtin(node):
    match str(node):
        case '+':
            op_node = vy_nodes.Add(node_id=next_nodeid(), ast_type='Add', _pretty="+", _description="addition")
            return op_node
        case '-':
            op_node = vy_nodes.Sub(node_id=next_nodeid(), ast_type='Sub', _pretty="-", _description="subtraction")
            return op_node
        case '*':
            op_node = vy_nodes.Mult(node_id=next_nodeid(), ast_type='Mult', _pretty="*", _description="multiplication")
            return op_node
        case '/':
            op_node = vy_nodes.Div(node_id=next_nodeid(), ast_type='Div', _pretty="/", _description="multiplication")
            return op_node

def parse_node(node):
    match node:
        case models.Expression(node):
            return parse_expr(node)
        case models.Integer(node):
            value_node = vy_nodes.Int(value=int(node), node_id=next_nodeid(), ast_type='Int')
            return value_node
        case models.Symbol(node) if str(node) in BUILTIN_FUNCS:
            return parse_builtin(node)
        case models.Symbol(node) | models.Keyword(node):
            name_node = vy_nodes.Name(id=str(node), node_id=next_nodeid(), ast_type='Name')
            return name_node
        case _:
            raise Exception(f"No match for node {node}")

def parse_src(src: str):
    ast = parse_node(hy.read(src))
    return ast
