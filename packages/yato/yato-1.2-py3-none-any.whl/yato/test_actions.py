import pytest
import json
from actions import createListList, ListNameEdit,\
    insert, changeListListPath, createConfig, new, addToList, changeListPath
import os
from pathlib import Path
from shutil import rmtree


@pytest.fixture(autouse=True)
def setup_teardown():
    # setup
    removeFiles = [
        'config.ini',
        'lists.json',
        'test.json',
        'test2.json',
        'asd.txt',
        '111.json',
        'testMoved.json',
        str(Path.home()) + os.path.sep + 'lists.json',
        str(Path.home()) + os.path.sep + 'testMoved.json'
    ]
    removePaths = [
        'listOfLists',
        'lists',
    ]

    # remove json files incase they exist
    for file in removeFiles:
        if os.path.exists(file):
            os.remove(file)
    # remove directories incase they exist
    for path in removePaths:
        print(path)
        if os.path.exists(path):
            rmtree(path)

    createConfig()
    createListList()

    yield  # runs tests

    # teardown
    for file in removeFiles:
        if os.path.exists(file):
            os.remove(file)
    for path in removePaths:

        if os.path.exists(path):
            rmtree(path)


def test_ListNameEdit():
    open('test.json', 'w').close()

    ListNameEdit('test.json', 'test2.json')
    assert os.path.exists('test2.json')
    assert ('test2.json' in json.loads(open('lists.json').read())['lists'])
    assert not ('test.json' in json.loads(open('lists.json').read())['lists'])

    ListNameEdit('test2.json', 'test2.json')
    assert os.path.exists('test2.json')
    assert ('test2.json' in json.loads(open('lists.json').read())['lists'])

    ListNameEdit('test2.json', 'asd.txt')
    assert os.path.exists('asd.txt')
    assert ('asd.txt' in json.loads(open('lists.json').read())['lists'])
    assert not ('test2.json' in json.loads(open('lists.json').read())['lists'])

    ListNameEdit('asd.txt', 'asd.txt')
    assert os.path.exists('asd.txt')
    assert ('asd.txt' in json.loads(open('lists.json').read())['lists'])

    ListNameEdit('asd.txt', '111.json')
    assert os.path.exists('111.json')
    assert ('111.json' in json.loads(open('lists.json').read())['lists'])
    assert not ('asd.txt' in json.loads(open('lists.json').read())['lists'])

    ListNameEdit('111.json', 'test.json')
    assert os.path.exists('test.json')
    assert ('test.json' in json.loads(open('lists.json').read())['lists'])
    assert not ('111.json' in json.loads(open('lists.json').read())['lists'])


def test_insert():

    new('test.json')
    insert('test.json', 'task', 1)
    assert json.loads(open('test.json').read())['tasks'][0] == ['task', 1]

    insert('test.json', 'task2', 2)

    assert json.loads(open('test.json').read())['tasks'][1] == ['task2', 2]

    insert('test.json', 'task1', 2)

    assert (json.loads(open('test.json').read())['tasks'][0] == ['task', 1])
    assert (json.loads(open('test.json').read())['tasks'][1] == ['task1', 2])
    assert (json.loads(open('test.json').read())['tasks'][2] == ['task2', 3])

    temp = json.loads(open('test.json').read())['tasks']

    insert('test.json', 'task3', 5)
    # should not change the list
    assert json.loads(open('test.json').read())['tasks'] == temp


def test_changeListListPath():
    sep = os.path.sep

    # Create 2 lists
    new('test.json')
    new('test2.json')

    # add tasks to lists
    addToList('test.json', 'task')
    addToList('test2.json', 'task2')

    # change path of listList
    changeListListPath('listList' + sep + 'listOfLists.json')
    # check if file exists
    assert(os.path.exists('listList' + sep + 'listOfLists.json'))
    # check if file was deleted
    assert(not os.path.exists('lists.json'))

    # check if the lists file's contents remain the same
    file = json.loads(open('listList' + sep + 'listOfLists.json').read())
    file = file['lists']
    assert('test.json' in file)
    assert('test2.json' in file)

    # move the lists file to home directory
    path = str(Path.home()) + os.path.sep + 'lists.json'
    # os.path.sep is the path separator, usually ' + sep + ' or \
    changeListListPath(path)
    # check if file exists
    assert(os.path.exists(path))
    # check if file was deleted
    assert(not os.path.exists('listList' + sep + 'listOfLists.json'))

    # check if the lists file's contents remain the same
    assert('test.json' in json.loads(open(path).read())['lists'])
    assert('test2.json' in json.loads(open(path).read())['lists'])


def test_createConfig():
    # check if config file exists
    assert os.path.exists('config.ini')
    # read config file
    temp = open('config.ini').read()
    # create config file (should not change the file)
    createConfig()
    # check if config file contents remain the same
    assert temp == open('config.ini').read()


def test_changeListPath():
    # create list
    new('test.json')

    # add task to lists
    addToList('test.json', 'task')

    # move and assert
    # save test.json as a variable
    temp = json.loads(open('test.json').read())
    # change path of list
    changeListPath('test.json', 'testMoved.json')
    # assert
    assert os.path.exists('testMoved.json')\
        and not os.path.exists('test.json')\
        and json.loads(open('testMoved.json').read()) == temp

    # move to folder lists and assert
    # save list as variable
    temp = json.loads(open('testMoved.json').read())
    # change path of list
    path = 'lists' + os.path.sep + 'testMoved.json'
    changeListPath('testMoved.json', path)
    # assert
    assert os.path.exists(path)\
        and not os.path.exists('testMoved.json')\
        and json.loads(open(path).read()) == temp

    # move to root directory and assert
    # save list as variable
    temp = json.loads(open('lists' + os.path.sep + 'testMoved.json').read())
    # change path of list
    prevPath = path
    path = str(Path.home()) + os.path.sep + 'testMoved.json'
    changeListPath(prevPath, path)
    # assert
    assert os.path.exists(path)\
        and not os.path.exists(prevPath)\
        and json.loads(open(path).read()) == temp
