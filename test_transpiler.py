from transpiler import transpile


def parse(*args):
    return "\n".join(args)


def test_declare():
    source = parse("x = 3")
    cpp = transpile(source)
    assert cpp == "auto x = 3;"


def test_assign():
    source = parse(
        "x = 3",
        "x = 1",
    )
    cpp = transpile(source)
    assert cpp == "auto x = 3;\nx = 1;"


def test_function_with_return():
    source = parse(
        "def fun(x):",
        "   return x",
    )
    cpp = transpile(source)
    print(cpp)
    assert cpp == ("template <typename T1>\n"
                   "auto fun(T1 x) {\n"
                   "return x;\n"
                   "}")


def test_list_as_vector():
    source = parse("values = [0, 1, 2, 3]")
    cpp = transpile(source)
    assert cpp == "std::vector<decltype(0)> values {0, 1, 2, 3};"


def test_vector_find_out_type():
    source = parse(
        "values = []",
        "values.append(1)",
    )
    cpp = transpile(source)
    assert cpp == ("std::vector<decltype(1)> values {};\n"
                   "values.push_back(1);")


def test_map_function():
    source = parse(
        "def map(values, fun):",
        "   results = []",
        "   for v in values:",
        "       results.append(fun(v))",
        "   return results",
    )
    cpp = transpile(source)
    assert cpp == ("template <typename T1, typename T2>\n"
                   "auto map(T1 values, T2 fun) {\n"
                   "std::vector<decltype(fun(declval"
                   "<decltype(values)::value_type>()))> results {};\n"
                   "for(auto v : values) {\n"
                   "results.push_back(fun(v));\n"
                   "}\n"
                   "return results;\n"
                   "}")
