import re
from pathlib import Path


def extract_festival_log_data(log_text: str) -> dict:
    # 1. 유효한 이메일 추출 (hyunwoo@.ac.kr처럼 도메인 라벨이 누락된 형식 제외)
    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b",
        log_text,
    )

    # 2. 휴대폰 번호 추출 (010 시작, 중간 4자리·끝 4자리, 구분자 -, ., 공백 허용)
    phones = re.findall(r"\b010[-.\s]\d{4}[-.\s]\d{4}\b", log_text)

    # 3. 본교 재학생 학번(202로 시작하는 9자리)과 학과명 튜플 추출
    students = re.findall(r"\[(202\d{6})\s*/\s*([^\]]+)\]", log_text)

    # 4-1. GitHub 저장소 URL 추출 (gitlab.com 제외)
    github_repos = re.findall(
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
        log_text,
    )

    # 4-2. 2026년 유효 쿠폰 코드 추출
    valid_coupons = re.findall(r"\bFEST-2026-[A-Z0-9]{4}\b", log_text)

    # 5. 부스별 총 매출액 추출('매출: ' 뒤 금액) 및 합산
    sales_matches = re.findall(r"매출:\s*([\d,]+)원", log_text)
    sales_amounts = [int(amount.replace(",", "")) for amount in sales_matches]
    total_sales = sum(sales_amounts)

    return {
        "emails": emails,
        "phones": phones,
        "students": students,
        "github_repos": github_repos,
        "valid_coupons": valid_coupons,
        "sales_amounts": sales_amounts,
        "total_sales": total_sales,
    }


def main() -> None:
    log_path = Path("07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt")
    log_text = log_path.read_text(encoding="utf-8")
    result = extract_festival_log_data(log_text)

    print("=== 1. 유효한 이메일 ===")
    for email in result["emails"]:
        print(f"  - {email}")

    print("\n=== 2. 휴대폰 번호 (010-XXXX-XXXX 형식) ===")
    for phone in result["phones"]:
        print(f"  - {phone}")

    print("\n=== 3. 본교 재학생 (학번, 학과) ===")
    for student in result["students"]:
        print(f"  - {student}")

    print("\n=== 4-1. GitHub 저장소 URL ===")
    for repo in result["github_repos"]:
        print(f"  - {repo}")

    print("\n=== 4-2. 2026 유효 쿠폰 ===")
    for coupon in result["valid_coupons"]:
        print(f"  - {coupon}")

    print("\n=== 5. 부스별 총 매출액 및 합계 ===")
    for amount in result["sales_amounts"]:
        print(f"  - {amount:,}원")
    print(f"  => 전체 매출 합계: {result['total_sales']:,}원")


if __name__ == "__main__":
    main()
