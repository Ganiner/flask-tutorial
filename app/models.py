from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # 如果你学过数据库的话就知道我们一般通过id来作为主键，来找到对应的信息的,通过id来实现唯一性
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return 'users表: id为:{}, name为:{}'.format(self.id, self.name)
