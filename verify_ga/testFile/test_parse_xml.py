from xml.dom.minidom import parse
cov_xml_path = "/home/steed/Desktop/session_work/IntroClass/grade/tests/cov.xml"


def parse_xml_and_get_rate():
    rootNode = parse(cov_xml_path).documentElement
    line_rate = rootNode.getAttribute("line-rate")  # 行覆盖率
    branch_rate = rootNode.getAttribute("branch-rate")  # 分支覆盖率
    lines_covered = rootNode.getAttribute("lines-covered")  # 覆盖行数
    branches_covered = rootNode.getAttribute("branches-covered")  # 覆盖分支数

    lineElements = rootNode.getElementsByTagName("line")
    line_list = [str(i) for i in range(1, int(lineElements[-1].getAttribute("number")) + 1)]
    hits_list = ["*"] * int(lineElements[-1].getAttribute("number"))
    for line in lineElements:
        # print(line.getAttribute("number"), line.getAttribute("hits"))
        hits_list[int(line.getAttribute("number"))-1] = line.getAttribute("hits")
    print(line_list)
    print(hits_list)

    # todo: 2020.3.6
if __name__ == '__main__':
    parse_xml_and_get_rate()