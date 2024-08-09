import pytest
from core.models.students import Student

@pytest.fixture
def existing_student():
    # we need atleast one student already present
    return Student.query.first()

def test_student_repr(existing_student):
    student = existing_student
    repr_output = repr(student)
    expected_repr = f'<Student {student.id!r}>'
    assert repr_output == expected_repr

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_without_principal_header(client, h_student_1):
    """
    failure case: principal not found
    """
    response = client.get(
        '/student/assignments',
    )
    assert response.status_code == 401

def test_get_assignments_student_with_principal_header_teacher(client, h_teacher_1):
    """
    failure case: Wrong principal header sent
    """
    response = client.get(
        '/student/assignments',
        headers=h_teacher_1
    )
    assert response.status_code == 403

def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'


def test_submit_assignment_missing_fields(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={}
    )
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'

def test_upsert_existing_assignment(client, h_student_1):
    # Create a draft assignment
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={'content': 'Initial content'}
    )
    assert response.status_code == 200
    draft_assignment = response.json['data']
    assignment_id = draft_assignment['id']
    
    # Upsert the existing assignment with new content
    new_content = 'Updated content'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': assignment_id,
            'content': new_content
        })
    
    assert response.status_code == 200
    updated_assignment = response.json['data']
    assert updated_assignment['content'] == new_content
    assert updated_assignment['state'] == 'DRAFT'  # Ensure the state is still DRAFT