# testone




test
./XXXX/manage.py test tests.test_xxxx_api.xxxxxxAPITestCase

测试发现基于 unittest 模块的 内置测试发现。默认情况下，它将在当前工作目录下的任何文件中发现名称为 test*.py 的测试。

你可以通过向 ./manage.py test 提供任意数量的 "测试标签" 来指定要运行的特定测试。每个测试标签可以是指向包、模块、TestCase 子类或测试方法的完整 Python 路径。例如：

# Run all the tests in the animals.tests module
$ ./manage.py test animals.tests

# Run all the tests found within the 'animals' package
$ ./manage.py test animals

# Run just one test case
$ ./manage.py test animals.tests.AnimalTestCase

# Run just one test method
$ ./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak
