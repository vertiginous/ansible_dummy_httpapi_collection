import pytest
from unittest.mock import patch, MagicMock
# from dummy_smtp import SMTPModule  # Replace with your actual module name
from plugins.modules import dummy_smtp


@pytest.fixture
def mock_connection():
    with patch('dummy_smtp.connection') as mock_conn:  # Replace 'dummy_smtp' with your actual module name
        yield mock_conn

def test_get_smtp_configuration(mock_connection):
    # Arrange
    mock_connection.get.return_value = {
        'enabled': True,
        'encrypted': True,
        'port': 587,
        'recipients': 'recipient@example.com',
        'server': 'smtp.example.com',
        'user': 'smtp_user'
    }
    
    # Act
    smtp_config = SMTPModule.get_smtp_configuration()
    
    # Assert
    assert smtp_config['port'] == 587
    assert smtp_config['enabled'] is True

def test_update_smtp_configuration(mock_connection):
    # Arrange
    smtp_config = {
        'enabled': True,
        'encrypted': True,
        'password': 'new_password',
        'port': 587,
        'recipients': 'recipient@example.com',
        'sender_email': 'sender@example.com',
        'server': 'smtp.example.com',
        'user': 'smtp_user'
    }
    
    mock_connection.put.return_value = smtp_config
    
    # Act
    updated_config = SMTPModule.update_smtp_configuration(smtp_config)
    
    # Assert
    assert updated_config['server'] == 'smtp.example.com'
    assert updated_config['port'] == 587

def test_delete_smtp_configuration(mock_connection):
    # Arrange
    mock_connection.delete.return_value = {'message': 'SMTP configuration deleted'}
    
    # Act
    response = SMTPModule.delete_smtp_configuration()
    
    # Assert
    assert response['message'] == 'SMTP configuration deleted'

