from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128))
    gender = db.Column(db.String(16))
    birth_date = db.Column(db.String(32))
    death_date = db.Column(db.String(32))
    bio = db.Column(db.Text)

    marriages = db.relationship('Marriage',
                                back_populates='person',
                                foreign_keys='Marriage.person_id')
    marriages_partner = db.relationship('Marriage',
                                        back_populates='partner',
                                        foreign_keys='Marriage.partner_id')

    children = db.relationship('ChildParent',
                               back_populates='parent',
                               foreign_keys='ChildParent.parent_id')
    parents = db.relationship('ChildParent',
                              back_populates='child',
                              foreign_keys='ChildParent.child_id')


class Marriage(db.Model):
    __tablename__ = 'marriage'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    marriage_date = db.Column(db.String(32))
    divorce_date = db.Column(db.String(32))

    person = db.relationship('Person', foreign_keys=[person_id], back_populates='marriages')
    partner = db.relationship('Person', foreign_keys=[partner_id], back_populates='marriages_partner')

    branch_id = db.Column(db.Integer, db.ForeignKey('tree_branch.id'))
    branch = db.relationship('TreeBranch', back_populates='marriages')

class ChildParent(db.Model):
    __tablename__ = 'child_parent'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    parent = db.relationship('Person', foreign_keys=[parent_id], back_populates='children')
    child = db.relationship('Person', foreign_keys=[child_id], back_populates='parents')


class TreeBranch(db.Model):
    __tablename__ = 'tree_branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)

    marriages = db.relationship('Marriage', back_populates='branch')
