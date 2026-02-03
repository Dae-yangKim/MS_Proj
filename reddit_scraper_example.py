import praw
import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------------
# [설정 필요] 본인의 API 키로 대체해야 합니다.
# https://www.reddit.com/prefs/apps 에서 생성 가능 (script 모드)
# -------------------------------------------------------------------------
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
USER_AGENT = 'script:my_reddit_scraper:v1.0 (by /u/YOUR_USERNAME)'

def scrape_reddit(target_subreddit, search_keyword, post_limit=10):
    """
    특정 서브레딧에서 키워드로 검색하여 게시글 및 댓글을 수집하는 함수
    """
    
    # 1. Reddit 인스턴스 생성
    # PRAW(Python Reddit API Wrapper)를 사용하여 Reddit API에 연결합니다.
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    
    # 2. 수집 시작 알림 (아이콘 추가)
    print(f"\n🚀 Reddit 데이터 수집 시작")
    print(f"🎯 Target Subreddit : {target_subreddit}")
    print(f"🔍 Search Keyword   : {search_keyword}")
    print(f"🔢 Post Limit       : {post_limit}\n")
    
    try:
        # 3. 서브레딧 접근 및 검색
        subreddit = reddit.subreddit(target_subreddit)
        
        # search() 메서드는 제너레이터를 반환합니다.
        # q: 검색어, limit: 가져올 게시글 수
        search_results = subreddit.search(q=search_keyword, limit=post_limit)
        
        data = []
        
        for post in search_results:
            # 게시글 정보 추출
            # datetime.fromtimestamp를 사용하여 유닉스 타임스탬프를 읽기 쉬운 시간으로 변환
            created_time = datetime.fromtimestamp(post.created_utc)
            
            post_data = {
                'title': post.title,
                'url': post.url,
                'score': post.score,
                'created_at': created_time,
                'num_comments': post.num_comments,
                'body': post.selftext,
                'comments': []
            }
            
            # 댓글 수집
            # replace_more(limit=0)은 'Load more comments' 객체를 처리하지 않고(시간 절약)
            # 현재 로드된 댓글 트리만 가져옵니다. 필요 시 limit을 늘릴 수 있습니다.
            post.comments.replace_more(limit=0) 
            
            for comment in post.comments:
                post_data['comments'].append(comment.body)
                
            data.append(post_data)
            print(f"✅ 수집 완료: {post.title[:30]}...")
            
        return data

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        return []

if __name__ == "__main__":
    # 사용 예시
    SUBREDDIT_NAME = "python"
    KEYWORD = "learning"
    LIMIT = 3
    
    # pip install praw pandas
    # 실행 전 위 CLIENT_ID 등을 본인 키로 채워주세요.
    results = scrape_reddit(SUBREDDIT_NAME, KEYWORD, LIMIT)
    
    if results:
        print(f"\n🎉 총 {len(results)}개의 게시글을 성공적으로 수집했습니다.")
        
        # (선택 사항) 데이터프레임 변환 및 확인
        # df = pd.DataFrame(results)
        # print(df.head())
    else:
        print("\n⚠️ 수집된 데이터가 없거나 에러가 발생했습니다.")
