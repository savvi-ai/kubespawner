from kubespawner import KubeSpawner

import pytest

_test_profiles = [
    {
        'display_name': 'Training Env - Python',
        'default': True,
        'kubespawner_override': {
            'image': 'training/python:label',
            'cpu_limit': 1,
            'mem_limit': 512 * 1024 * 1024,
            }
    },
    {
        'display_name': 'Training Env - Datascience',
        'kubespawner_override': {
            'image': 'training/datascience:label',
            'cpu_limit': 4,
            'mem_limit': 8 * 1024 * 1024 * 1024,
            }
    },
]


@pytest.mark.asyncio
async def test_user_options_api_with_memory_cpu():
    spawner = KubeSpawner(_mock=True)
    spawner.profile_list = _test_profiles

    cpu_limit = 1
    mem_limit = 4 * 1024 * 1024 * 1024

    # set user_options directly (e.g. via api)
    spawner.user_options = {'profile': _test_profiles[1]['display_name'], 'cpu_limit': cpu_limit, 'mem_limit': mem_limit}

    # nothing should be loaded yet
    assert spawner.cpu_limit is None
    assert spawner.mem_limit is None

    await spawner.load_user_options()
    for key, value in _test_profiles[1]['kubespawner_override'].items():
        if key == 'cpu_limit' or key == 'mem_limit':
            continue
        assert getattr(spawner, key) == value

    assert spawner.cpu_limit == float(cpu_limit)
    assert spawner.mem_limit == mem_limit

@pytest.mark.asyncio
async def test_user_options_api_with_cpu_float():
    spawner = KubeSpawner(_mock=True)
    spawner.profile_list = _test_profiles

    cpu_limit = 1

    # set user_options directly (e.g. via api)
    spawner.user_options = {'profile': _test_profiles[1]['display_name'], 'cpu_limit': cpu_limit}

    # nothing should be loaded yet
    assert spawner.cpu_limit is None
    assert spawner.mem_limit is None

    await spawner.load_user_options()
    for key, value in _test_profiles[1]['kubespawner_override'].items():
        if key == 'cpu_limit' or key == 'mem_limit':
            continue
        assert getattr(spawner, key) == value

    assert spawner.cpu_limit == cpu_limit
    assert spawner.mem_limit == 8 * 1024 * 1024 * 1024
