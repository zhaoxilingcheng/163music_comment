import json
import random
import time
from models import *

import jieba
import requests
from simhash import Simhash, SimhashIndex

words1 = jieba.lcut('我很想要打游戏，但是女朋友会生气！', cut_all=True)
words2 = jieba.lcut('我很想要打游戏，但是女朋友非常生气！', cut_all=True)

print(Simhash(words1).distance(Simhash(words2)))

headers = {
    'authority': 'music.163.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'nm-gcore-status': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'origin': 'https://music.163.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://music.163.com/discover/recommend/taste',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie': 'NMTID=00OPPqSQfeQRWJC_kgIlKN8tEzH-zEAAAF3Tf2piw; _iuqxldmzr_=32; _ntes_nnid=2b3bf783fe3880efcb13266ca0d38bc3,1611921212626; _ntes_nuid=2b3bf783fe3880efcb13266ca0d38bc3; WM_TID=9o8J6QcWh%2BZAVREAFEZ%2Fb0fnomJ1jxE8; ne_analysis_trace_id=1613962381191; s_n_f_l_n3=bf4889d1818193f21613962381199; vinfo_n_f_l_n3=bf4889d1818193f2.1.1.1611537908632.1611717355015.1613962500890; _ns=NS1.2.496380456.1614328135; UserProvince=%u5168%u56FD; JSESSIONID-WYYY=fp%2BszRofExJk%2BziYHpHgsnSIJDm6dyze4mFaqApxKsnHcK%5CnGojSxl%2FnNqs%5CVMu1yEgPMrdWkS3OSHKcy0DqEcfKS8PqZGxI04xHJ4eG4iQZ3M0w5OQi6yy3SZ0wYRBv4nNTc1IDPZM%5C4jZz5IoEDuOWfF45iM9eZ8yNoFtB2%5CgYYQbu%3A1614569922402; WNMCID=tzucct.1614568122836.01.0; WEVNSM=1.0.0; WM_NI=G0%2Fv3xyarvMwodEtW1Bbjetl6PevVCnR27%2BGFSPjDqxqE4bmghTHJGpuK6CX1thttdt1McwkBpEGy3XoOCuyLfYyuAv9MTacfh2O8LURYYeZXQkiq1UW5uDZ1JrbyJE5Sko%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb0c65db08efd90f65087e78aa2d14b939b8eaff46bf6a78190d87dad9db8bbf72af0fea7c3b92a85f0e197b274bbbfbe97d07dadbc8b95d63b82bea686f768f690ab97d549ae8efed8aa4d868da08bc77bbcaf8bd5e167a5b89ca9c94db4ab85d7c254f3aca895f770b8ef8384f66182b08ba8fc399cb181a4f87390ba979af84bb6e783b5e469a6b8feb0bb48978e97bae8529c8fa58af43b9789fb96c752f396be83fc4287eb9d8cee37e2a3; __remember_me=true; __csrf=87fc709ba7a5132fa6359178e1ce1c37; MUSIC_U=b4ac0733049815e5d2b882998abd4a98780c096322ba268e47e1d6244c40a6a733a649814e309366',
}

params = (
    ('csrf_token', '87fc709ba7a5132fa6359178e1ce1c37'),
)

data = {
    'params': 'KxlpLPGXydXfj0Wid1D6y9j2jBdrHSXfCovE+3BeRVG0+H4XSqM+AlEJVe92oMfLzfbxeFrP2nnJJXMbM4JhP6Fs+68V6BaXXXUNJq3EQNQwT4zxHKMtqpG8dDl5eOgCvsimIv7blxVKIY6VFAHOWg==',
    'encSecKey': '670acd0d0945f6aceeba5fb093d7e781eef13837a4a034cbb0fea8be06787b7bd01b70b7056c72c96727613834c9b44d665037338d46b10acd30c915e49dc221fe35d7b06641de508b4c4e77ab536b1256c4951e4473beea5ff037720f4fa3112fa7aaca3da827c13e295a7621944dbf46520c35f1f7f2102cedaafc30ea58ec'
}


def get_song_data(song):
    s = Song()
    s.song_id = song['id']
    s.comment_thread_id = song['commentThreadId']
    s.name = song['name']
    return s


def get_songs():
    songs_data_text = requests.post('https://music.163.com/weapi/v2/discovery/recommend/songs', headers=headers,
                                    params=params,
                                    data=data).text
    recommend = json.loads(songs_data_text)['recommend']
    return list(map(get_song_data, recommend))


def get_comment_data(comment):
    c = Comment()
    c.content = comment['content']
    c.like_count = comment['likedCount']
    c.comment_id = comment['commentId']
    c.simHash = Simhash(jieba.lcut(comment['content'], cut_all=True)).value
    return c


def get_comments(comment_thread_id):
    url = f'http://music.163.com/api/v1/resource/comments/{comment_thread_id}?offset=0&limit=20'
    comments_data_text = requests.get(url, headers=headers, params=params).text
    comments = json.loads(comments_data_text)['hotComments']
    return list(map(get_comment_data, comments))


def init_index():
    comments = Comment().select()
    print(comments)
    # SimhashIndex(, 3)


def launch():
    songs = get_songs()
    for i in songs:
        print(f'当前处理的音乐为{i.name}')
        i.save_()
        comments = get_comments(i.comment_thread_id)
        for comment in comments:
            print(f'爬取评论: {comment.content}')
            comment.song_id = i.song_id
            comment.save_()
        time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    launch()
    print(Song.select())
