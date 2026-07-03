from app import create_app
from app.models import db, Sentence

app = create_app()

with app.app_context():

    db.create_all()

    # 清空舊資料（避免重複）
    Sentence.query.delete()

    data = [
        Sentence(region="北部", gender="男", content="我喜歡打球"),
        Sentence(region="北部", gender="男", content="我喜歡寫程式"),
        Sentence(region="北部", gender="女", content="我喜歡喝咖啡"),
        Sentence(region="中部", gender="男", content="我喜歡爬山"),
        Sentence(region="南部", gender="女", content="我喜歡海邊"),
    ]

    db.session.add_all(data)
    db.session.commit()

    print("seed 完成")
    