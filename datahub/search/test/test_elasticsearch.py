from unittest import mock

from .. import elasticsearch


@mock.patch('datahub.search.elasticsearch.es_bulk')
def test_bulk(es_bulk, mock_es_client):
    """Tests detailed company search."""
    actions = []
    chunk_size = 10
    elasticsearch.bulk(actions=actions, chunk_size=chunk_size)

    es_bulk.assert_called_with(mock_es_client.return_value, actions=actions, chunk_size=chunk_size)


@pytest.mark.parametrize('expected', (True, False))
def test_index_exists(mock_es_client, expected):
    """Tests that `index_exists` returns True if the index exists, False otherwise."""
    index_name = 'test'

    connection = mock_es_client.return_value
    connection.indices.exists.return_value = expected

    assert elasticsearch.index_exists(name=index_name) == expected
    connection.indices.exists.assert_called_with(index=index_name)


@mock.patch('datahub.search.elasticsearch.settings')
@mock.patch('datahub.search.elasticsearch.connections')
def test_configure_connection(connections, settings):
    """Tests if Heroku connection is configured."""
    settings.HEROKU = True
    settings.ES_USE_AWS_AUTH = False
    settings.ES_URL = 'https://login:password@test:1234'
    connections.configure.return_value = {}

    elasticsearch.configure_connection()

    connections.configure.assert_called_with(default={
        'hosts': [settings.ES_URL],
        'verify_certs': settings.ES_VERIFY_CERTS
    })


def test_creates_index(mock_es_client):
    """Test creates_index()."""
    index = 'test-index'
    index_settings = {
        'testsetting1': 'testval1'
    }
    connection = mock_es_client.return_value
    elasticsearch.create_index(index, index_settings=index_settings)
    connection.indices.create.assert_called_once_with(
        index='test-index',
        body={
            'settings': {
                'testsetting1': 'testval1',
                'analysis': {
                    'analyzer': {
                        'lowercase_keyword_analyzer': {
                            'tokenizer': 'keyword',
                            'filter': ['lowercase'],
                            'type': 'custom'
                        },
                        'trigram_analyzer': {
                            'tokenizer': 'trigram',
                            'char_filter': ['special_chars'],
                            'filter': ['lowercase'],
                            'type': 'custom'
                        },
                        'english_analyzer': {
                            'tokenizer': 'standard',
                            'filter': [
                                'english_possessive_stemmer',
                                'lowercase',
                                'english_stop',
                                'english_stemmer'
                            ],
                            'type': 'custom'
                        },
                        'lowercase_analyzer': {
                            'tokenizer': 'standard',
                            'filter': ['lowercase'],
                            'type': 'custom'
                        }
                    },
                    'tokenizer': {
                        'trigram': {
                            'min_gram': 3,
                            'max_gram': 3,
                            'token_chars': ('letter', 'digit'),
                            'type': 'nGram'
                        }
                    },
                    'char_filter': {
                        'special_chars': {
                            'mappings': ('-=>',),
                            'type': 'mapping'}
                    },
                    'filter': {
                        'english_possessive_stemmer': {
                            'language': 'possessive_english',
                            'type': 'stemmer'
                        },
                        'english_stop': {
                            'stopwords': '_english_', 'type': 'stop'
                        },
                        'english_stemmer': {
                            'language': 'english', 'type': 'stemmer'
                        }
                    }
                }
            }
        }
    )


def test_configure_index_doesnt_create_index_if_it_exists(mock_es_client):
    """Test that configure_index() doesn't create the index when it already exists."""
    index = 'test-index'
    connection = mock_es_client.return_value
    assert elasticsearch.index_exists(index) is connection.indices.exists.return_value
