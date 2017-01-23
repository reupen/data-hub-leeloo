import uuid

import factory


class TaskInfoFactory(factory.django.DjangoModelFactory):
    """TaskInfo factory."""

    task_id = factory.Sequence(lambda x: '{0}'.format(uuid.uuid4()))
    changes = {'foo': 'bar'}
    update = True
    db_table = 'foo_bar'

    class Meta:
        model = 'core.TaskInfo'
