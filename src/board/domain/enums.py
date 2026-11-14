from enum import StrEnum

# 역할 정의
class Role(StrEnum) :
    """
    사용자 역할이자 리소스 접근에 필요한 최소 권한

    2가지 용도로 활용
    1. 사용자의 역할 : 
        - 요청한 사용자가 가진 권한 (비로그인 사용자는 ALL)
    2. 요구 권한 : 
        - 게시판 읽기/쓰기 등에 필요한 최소 권한
        - 권한은 계층 구조이며, 상위 역할은 하위 역할의 권한을  모두 포함
        - ADMIN(2) > USER(1) > ALL(0)
    """

    ALL = "ALL" # 비회원 포함 모두
    USER = "USER" # 회원 + 관리자
    ADMIN = "ADMIN" # 관리자만

    @property
    def level(self) -> int :
        """
        권한 비교에 사용하는 가중치
        값이 클수록 상위 권한
        """
        _levels = {
            Role.ALL : 0,
            Role.USER : 1,
            Role.ADMIN : 2,
        }
        return _levels[self]

    def satisfies(self, required_role : "Role | str") -> bool :
        """
        현재 역할이 요구 권한 이상을 보유하고 있는지 검증
        """
        if isinstance(required_role, str) :
            required_role = Role(required_role)

        return self.level >= required_role.level


# 게시글 검색 타입
class PostSearchType(StrEnum) :
    """
    게시글 검색 조건
    검색어를 어떤 필드에서 찾을지 지정
    """

    ALL = "ALL"
    TITLE = "TITLE"
    CONTENT = "CONTENT"
    TITLE_CONTENT = "TITLE_CONTENT"
    AUTHOR_NAME = "AUTHOR_NAME"
    AUTHOR_EMAIL = "AUTHOR_EMAIL"