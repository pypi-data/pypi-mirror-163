import os.path
import sys

api_run_content = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
"""

android_run_content = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        serial_no='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )
"""

ios_run_content = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        serial_no='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
"""

browser_run_content = """import qrunner


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents-pre.qizhidao.com'
    )
"""

case_content_android = """import qrunner
from qrunner.core.android import TestCase, Element


class HomePage:
    ad_close_btn = Element(rid='id/bottom_btn', desc='首页广告关闭按钮')
    bottom_my = Element(rid='id/bottom_view', index=3, desc='首页底部我的入口')


@qrunner.story('首页')
class TestAdrSample(TestCase):
    
    def start(self):
        self.hp = HomePage()
    
    @qrunner.title('从首页进入我的页')
    def test_go_my(self):
        self.hp.ad_close_btn.click()
        self.hp.bottom_my.click()
        self.assertText('我的订单')
"""

case_content_ios = """import qrunner
from qrunner.core.ios import TestCase, Element


class HomePage:
    ad_close_btn = Element(label='close white big', desc='首页广告关闭按钮')
    bottom_my = Element(label='我的', desc='首页底部我的入口')


@qrunner.story('首页')
class TestIosSample(TestCase):

    def start(self):
        self.hp = HomePage()

    @qrunner.title('从首页进入我的页')
    def test_go_my(self):
        self.hp.ad_close_btn.click()
        self.hp.bottom_my.click()
        self.assertText('我的订单')
"""

case_content_web = """import qrunner
from qrunner.core.web import TestCase, Element


class PatentPage:
    search_input = Element(tid='driver-home-step1', desc='查专利首页输入框')
    search_submit = Element(tid='driver-home-step2', desc='查专利首页搜索确认按钮')


@qrunner.story('专利检索')
class TestWebSample(TestCase):
    
    def start(self):
        self.pp = PatentPage()
    
    @qrunner.title('专利简单检索')
    def test_patent_search(self):
        self.open_url()
        self.pp.search_input.set_text('无人机')
        self.pp.search_submit.click()
        self.assertTitle('无人机专利检索-企知道')
"""

case_content_api = """import qrunner
from qrunner.core.api import TestCase


@qrunner.story('PC站首页')
class TestApiSample(TestCase):

    @qrunner.title('查询PC站首页banner列表')
    @qrunner.file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        load = {"type": card_type}
        self.post(path, json=load)
        self.assertEq('code', 0)
"""

require_content = """qrunner
"""

ignore_content = "\n".join(
    ["__pycache__/*", "*.pyc", ".idea/*", ".DS_Store", "allure-results", "images", ".pytest_cache"]
)

data_content = """{
  "card_type": [0, 1, 2]
}
"""


def init_scaffold_project(subparsers):
    parser = subparsers.add_parser("start", help="Create a new project with template structure.")
    parser.add_argument('-t', '--platform', dest='platform', type=str, default='api', help='测试平台: api、android、ios、web')
    return parser


def create_scaffold(platform):
    """ create scaffold with specified project name.
    """

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    project_name = f'{platform}_demo'
    create_folder(project_name)
    create_file(
        os.path.join(project_name, ".gitignore"),
        ignore_content,
    )
    create_file(
        os.path.join(project_name, "requirements.txt"),
        require_content,
    )
    create_folder(os.path.join(project_name, 'test_dir'))
    create_folder(os.path.join(project_name, 'test_data'))
    create_folder(os.path.join(project_name, 'test_dir', 'common'))
    create_folder(os.path.join(project_name, 'test_dir', 'test_case'))
    create_file(
        os.path.join(project_name, 'test_dir', "__init__.py"),
        '',
    )
    create_file(
        os.path.join(project_name, 'test_dir', 'test_case', "__init__.py"),
        '',
    )
    create_file(
        os.path.join(project_name, 'test_dir', 'common', "__init__.py"),
        '',
    )
    create_file(
        os.path.join(project_name, 'test_data', "data.json"),
        data_content,
    )
    if platform == 'api':
        create_file(
            os.path.join(project_name, "run.py"),
            api_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', 'test_case', "test_api_sample.py"),
            case_content_api,
        )
    elif platform == 'android':
        create_file(
            os.path.join(project_name, "run.py"),
            android_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', 'test_case', "test_adr_sample.py"),
            case_content_android,
        )
    elif platform == 'ios':
        create_file(
            os.path.join(project_name, "run.py"),
            ios_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', 'test_case', "test_ios_sample.py"),
            case_content_ios,
        )
    elif platform == 'web':
        create_file(
            os.path.join(project_name, "run.py"),
            browser_run_content,
        )
        create_file(
            os.path.join(project_name, 'test_dir', 'test_case', "test_web_sample.py"),
            case_content_web,
        )
    else:
        print(f'不支持的平台: {platform}')
        sys.exit()
    return 0


def main_scaffold_project(args):
    sys.exit(create_scaffold(args.platform))

