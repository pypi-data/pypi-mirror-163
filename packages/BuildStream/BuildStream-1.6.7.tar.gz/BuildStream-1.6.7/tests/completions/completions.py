import os
import pytest
from tests.testutils import cli

# Project directory
DATA_DIR = os.path.dirname(os.path.realpath(__file__))

MAIN_COMMANDS = [
    'build ',
    'checkout ',
    'fetch ',
    'help ',
    'init ',
    'pull ',
    'push ',
    'shell ',
    'show ',
    'source-bundle ',
    'track ',
    'workspace '
]

MAIN_OPTIONS = [
    "--builders ",
    "-c ",
    "-C ",
    "--colors ",
    "--config ",
    "--debug ",
    "--default-mirror ",
    "--directory ",
    "--error-lines ",
    "--fetchers ",
    "--log-file ",
    "--max-jobs ",
    "--message-lines ",
    "--network-retries ",
    "--no-colors ",
    "--no-debug ",
    "--no-interactive ",
    "--no-strict ",
    "--no-verbose ",
    "-o ",
    "--option ",
    "--on-error ",
    "--pushers ",
    "--strict ",
    "--verbose ",
    "--version ",
]

WORKSPACE_COMMANDS = [
    'close ',
    'list ',
    'open ',
    'reset '
]

PROJECT_ELEMENTS = [
    "compose-all.bst",
    "compose-exclude-dev.bst",
    "compose-include-bin.bst",
    "import-bin.bst",
    "import-dev.bst",
    "target.bst"
]


def assert_completion(cli, cmd, word_idx, expected, cwd=None):
    result = cli.run(cwd=cwd, env={
        '_BST_COMPLETION': 'complete',
        'COMP_WORDS': cmd,
        'COMP_CWORD': str(word_idx)
    })
    words = []
    if result.output:
        words = result.output.splitlines()

    # The order is meaningless, bash will
    # take the results and order it by it's
    # own little heuristics
    words = sorted(words)
    expected = sorted(expected)
    assert words == expected


@pytest.mark.parametrize("cmd,word_idx,expected", [
    ('bst', 0, []),
    ('bst ', 1, MAIN_COMMANDS),
    ('bst pu', 1, ['pull ', 'push ']),
    ('bst pul', 1, ['pull ']),
    ('bst w ', 1, ['workspace ']),
    ('bst workspace ', 2, WORKSPACE_COMMANDS),
])
def test_commands(cli, cmd, word_idx, expected):
    assert_completion(cli, cmd, word_idx, expected)


@pytest.mark.parametrize("cmd,word_idx,expected", [
    ('bst -', 1, MAIN_OPTIONS),
    ('bst --l', 1, ['--log-file ']),

    # Test that options of subcommands also complete
    ('bst --no-colors build -', 3, ['--all ', '--track ', '--track-all ',
                                    '--track-except ',
                                    '--track-cross-junctions ', '-J ',
                                    '--track-save ']),

    # Test the behavior of completing after an option that has a
    # parameter that cannot be completed, vs an option that has
    # no parameter
    ('bst --fetchers ', 2, []),
    ('bst --no-colors ', 2, MAIN_COMMANDS),
])
def test_options(cli, cmd, word_idx, expected):
    assert_completion(cli, cmd, word_idx, expected)


@pytest.mark.parametrize("cmd,word_idx,expected", [
    ('bst --on-error ', 2, ['continue ', 'quit ', 'terminate ']),
    ('bst show --deps ', 3, ['all ', 'build ', 'none ', 'plan ', 'run ']),
    ('bst show --deps=', 2, ['all ', 'build ', 'none ', 'plan ', 'run ']),
    ('bst show --deps b', 3, ['build ']),
    ('bst show --deps=b', 2, ['build ']),
    ('bst show --deps r', 3, ['run ']),
    ('bst track --deps ', 3, ['all ', 'none ']),
])
def test_option_choice(cli, cmd, word_idx, expected):
    assert_completion(cli, cmd, word_idx, expected)


@pytest.mark.datafiles(os.path.join(DATA_DIR, 'project'))
@pytest.mark.parametrize("cmd,word_idx,expected,subdir", [
    # Note that elements/ and files/ are partial completions and
    # as such do not come with trailing whitespace
    ('bst --config ', 2, ['cache/', 'elements/', 'files/', 'project.conf '], None),
    ('bst --log-file ', 2, ['cache/', 'elements/', 'files/', 'project.conf '], None),
    ('bst --config f', 2, ['files/'], None),
    ('bst --log-file f', 2, ['files/'], None),
    ('bst --config files', 2, ['files/bin-files/', 'files/dev-files/'], None),
    ('bst --log-file files', 2, ['files/bin-files/', 'files/dev-files/'], None),
    ('bst --config files/', 2, ['files/bin-files/', 'files/dev-files/'], None),
    ('bst --log-file elements/', 2, [os.path.join('elements', e) + ' ' for e in PROJECT_ELEMENTS], None),
    ('bst --config ../', 2, ['../cache/', '../elements/', '../files/', '../project.conf '], 'files'),
    ('bst --config ../elements/', 2, [os.path.join('..', 'elements', e) + ' ' for e in PROJECT_ELEMENTS], 'files'),
    ('bst --config ../nofile', 2, [], 'files'),
    ('bst --config /pony/rainbow/nobodyhas/this/file', 2, [], 'files'),
])
def test_option_file(datafiles, cli, cmd, word_idx, expected, subdir):
    cwd = str(datafiles)
    if subdir:
        cwd = os.path.join(cwd, subdir)
    assert_completion(cli, cmd, word_idx, expected, cwd=cwd)


@pytest.mark.datafiles(os.path.join(DATA_DIR, 'project'))
@pytest.mark.parametrize("cmd,word_idx,expected,subdir", [
    # Note that regular files like project.conf are not returned when
    # completing for a directory
    ('bst --directory ', 2, ['cache/', 'elements/', 'files/'], None),
    ('bst --directory elements/', 2, [], None),
    ('bst --directory ', 2, ['dev-files/', 'bin-files/'], 'files'),
    ('bst --directory ../', 2, ['../cache/', '../elements/', '../files/'], 'files'),
])
def test_option_directory(datafiles, cli, cmd, word_idx, expected, subdir):
    cwd = str(datafiles)
    if subdir:
        cwd = os.path.join(cwd, subdir)
    assert_completion(cli, cmd, word_idx, expected, cwd=cwd)


@pytest.mark.datafiles(DATA_DIR)
@pytest.mark.parametrize("project,cmd,word_idx,expected,subdir", [
    # When running in the project directory
    ('project', 'bst show ', 2, [e + ' ' for e in PROJECT_ELEMENTS], None),
    ('project', 'bst build com', 2,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], None),

    # When running from the files subdir
    ('project', 'bst show ', 2, [e + ' ' for e in PROJECT_ELEMENTS], 'files'),
    ('project', 'bst build com', 2,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], 'files'),

    # When passing the project directory
    ('project', 'bst --directory ../ show ', 4, [e + ' ' for e in PROJECT_ELEMENTS], 'files'),
    ('project', 'bst --directory ../ build com', 4,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], 'files'),

    # Also try multi arguments together
    ('project', 'bst --directory ../ checkout t ', 4, ['target.bst '], 'files'),
    ('project', 'bst --directory ../ checkout target.bst ', 5, ['bin-files/', 'dev-files/'], 'files'),

    # When running in the project directory
    ('no-element-path', 'bst show ', 2,
     [e + ' ' for e in (PROJECT_ELEMENTS + ['project.conf'])] + ['files/'], None),
    ('no-element-path', 'bst build com', 2,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], None),

    # When running from the files subdir
    ('no-element-path', 'bst show ', 2,
     [e + ' ' for e in (PROJECT_ELEMENTS + ['project.conf'])] + ['files/'], 'files'),
    ('no-element-path', 'bst build com', 2,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], 'files'),

    # When passing the project directory
    ('no-element-path', 'bst --directory ../ show ', 4,
     [e + ' ' for e in (PROJECT_ELEMENTS + ['project.conf'])] + ['files/'], 'files'),
    ('no-element-path', 'bst --directory ../ show f', 4, ['files/'], 'files'),
    ('no-element-path', 'bst --directory ../ show files/', 4, ['files/bin-files/', 'files/dev-files/'], 'files'),
    ('no-element-path', 'bst --directory ../ build com', 4,
     ['compose-all.bst ', 'compose-include-bin.bst ', 'compose-exclude-dev.bst '], 'files'),

    # Also try multi arguments together
    ('no-element-path', 'bst --directory ../ checkout t ', 4, ['target.bst '], 'files'),
    ('no-element-path', 'bst --directory ../ checkout target.bst ', 5, ['bin-files/', 'dev-files/'], 'files'),

    # When element-path have sub-folders
    ('sub-folders', 'bst show base', 2, ['base/wanted.bst '], None),
    ('sub-folders', 'bst show base/', 2, ['base/wanted.bst '], None),
])
def test_argument_element(datafiles, cli, project, cmd, word_idx, expected, subdir):
    cwd = os.path.join(str(datafiles), project)
    if subdir:
        cwd = os.path.join(cwd, subdir)
    assert_completion(cli, cmd, word_idx, expected, cwd=cwd)


@pytest.mark.parametrize("cmd,word_idx,expected", [
    ('bst he', 1, ['help ']),
    ('bst help ', 2, MAIN_COMMANDS),
    ('bst help fe', 2, ['fetch ']),
    ('bst help p', 2, ['pull ', 'push ']),
    ('bst help p', 2, ['pull ', 'push ']),
    ('bst help w', 2, ['workspace ']),
    ('bst help workspace ', 3, WORKSPACE_COMMANDS),
])
def test_help_commands(cli, cmd, word_idx, expected):
    assert_completion(cli, cmd, word_idx, expected)
