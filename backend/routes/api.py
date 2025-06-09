from flask import Blueprint, request, jsonify
from models import db, Person, Marriage, ChildParent, TreeBranch

api_blueprint = Blueprint('api', __name__)

# Отримати всіх людей
@api_blueprint.route('/person', methods=['GET'])
def get_all_people():
    people = Person.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'surname': p.surname,
        'gender': p.gender,
        'birth_date': p.birth_date,
        'death_date': p.death_date,
        'bio': p.bio
    } for p in people])

# Отримати одну людину
@api_blueprint.route('/person/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if not person:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id': person.id,
        'name': person.name,
        'surname': person.surname,
        'gender': person.gender,
        'birth_date': person.birth_date,
        'death_date': person.death_date,
        'bio': person.bio
    })

# Додати нову людину
@api_blueprint.route('/person', methods=['POST'])
def add_person():
    data = request.json
    person = Person(
        name=data.get('name'),
        surname=data.get('surname'),
        gender=data.get('gender'),
        birth_date=data.get('birth_date'),
        death_date=data.get('death_date'),
        bio=data.get('bio')
    )
    db.session.add(person)
    db.session.commit()
    return jsonify({'message': 'Person added', 'id': person.id}), 201

# Редагувати людину
@api_blueprint.route('/person/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = Person.query.get(person_id)
    if not person:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    person.name = data.get('name', person.name)
    person.surname = data.get('surname', person.surname)
    person.gender = data.get('gender', person.gender)
    person.birth_date = data.get('birth_date', person.birth_date)
    person.death_date = data.get('death_date', person.death_date)
    person.bio = data.get('bio', person.bio)
    db.session.commit()
    return jsonify({'message': 'Person updated'})

# Видалити людину
@api_blueprint.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if not person:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'Person deleted'})

# Подібні CRUD для Marriage, ChildParent, TreeBranch — за аналогією

# Приклад: отримати всі шлюби
@api_blueprint.route('/marriage', methods=['GET'])
def get_all_marriages():
    marriages = Marriage.query.all()
    return jsonify([{
        'id': m.id,
        'person_id': m.person_id,
        'partner_id': m.partner_id,
        'marriage_date': m.marriage_date,
        'divorce_date': m.divorce_date,
        'branch_id': m.branch_id
    } for m in marriages])

# Отримати всі гілки дерева
@api_blueprint.route('/branch', methods=['GET'])
def get_all_branches():
    branches = TreeBranch.query.all()
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'description': b.description
    } for b in branches])

# Отримати дітей певної людини
@api_blueprint.route('/person/<int:person_id>/children', methods=['GET'])
def get_children(person_id):
    links = ChildParent.query.filter_by(parent_id=person_id).all()
    children = []
    for link in links:
        child = Person.query.get(link.child_id)
        if child:
            children.append({
                'id': child.id,
                'name': child.name,
                'surname': child.surname,
                'gender': child.gender
            })
    return jsonify(children)

# Отримати батьків певної людини
@api_blueprint.route('/person/<int:person_id>/parents', methods=['GET'])
def get_parents(person_id):
    links = ChildParent.query.filter_by(child_id=person_id).all()
    parents = []
    for link in links:
        parent = Person.query.get(link.parent_id)
        if parent:
            parents.append({
                'id': parent.id,
                'name': parent.name,
                'surname': parent.surname,
                'gender': parent.gender
            })
    return jsonify(parents)
