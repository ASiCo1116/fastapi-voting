from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = list(map(lambda post: schemas.PostOut(**post), res.json()))

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)
