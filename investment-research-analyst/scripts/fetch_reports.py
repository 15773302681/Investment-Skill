#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研报爬取脚本 - 获取东方财富等平台的行业研报
"""

import argparse
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class ReportFetcher:
    """研报爬取器"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_eastmoney_reports(self, industry: str, days: int = 30) -> List[Dict]:
        """
        获取东方财富网的行业研报

        Args:
            industry: 行业名称
            days: 获取近N天的研报

        Returns:
            研报列表，每个元素包含标题、机构、日期、摘要、链接
        """
        try:
            # 东方财富研报URL
            url = "http://data.eastmoney.com/report/hyyb.js"
            params = {
                'industryCode': '',
                'startDate': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'endDate': datetime.now().strftime('%Y-%m-%d'),
                'pageNum': '1',
                'pageSize': '50'
            }

            print(f"正在获取东方财富网研报，行业: {industry}，时间范围: 近{days}天")

            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()

            # 解析JS数据（实际是JSONP格式）
            content = response.text
            # 提取JSON部分
            json_start = content.find('(') + 1
            json_end = content.rfind(')')
            json_str = content[json_start:json_end]

            import json
            data = json.loads(json_str)

            reports = []
            if 'data' in data and 'diff' in data['data']:
                for item in data['data']['diff']:
                    # 筛选包含行业关键词的研报
                    title = item.get('title', '')
                    industry_field = item.get('industry', '')

                    if industry.lower() in title.lower() or industry.lower() in industry_field.lower():
                        report = {
                            'title': title,
                            'institution': item.get('orgName', ''),
                            'date': item.get('publishDate', ''),
                            'rating': item.get('rating', ''),
                            'summary': item.get('abstract', ''),
                            'url': f"http://data.eastmoney.com/report/detail/{item.get('infoCode', '')}.html"
                        }
                        reports.append(report)

            print(f"成功获取 {len(reports)} 篇相关研报")
            return reports

        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {str(e)}")
            return []
        except Exception as e:
            print(f"解析数据失败: {str(e)}")
            return []

    def fetch_sina_reports(self, industry: str, days: int = 30) -> List[Dict]:
        """
        获取新浪财经的研报数据（备用）

        Args:
            industry: 行业名称
            days: 获取近N天的研报

        Returns:
            研报列表
        """
        try:
            url = "https://vip.stock.finance.sina.com.cn/corp/view/vRP_NewStockReportDetail.php"
            params = {
                'stockid': '',
                'page': '1'
            }

            print(f"尝试获取新浪财经研报...")

            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')
            reports = []

            # 解析研报列表（根据实际HTML结构调整）
            # 此处为示例逻辑，需根据实际页面结构调整
            report_items = soup.find_all('div', class_='report-item')

            for item in report_items:
                title_tag = item.find('a')
                if title_tag and industry.lower() in title_tag.text.lower():
                    report = {
                        'title': title_tag.text.strip(),
                        'institution': item.find('span', class_='institution').text.strip(),
                        'date': item.find('span', class_='date').text.strip(),
                        'summary': '',
                        'url': title_tag.get('href', '')
                    }
                    reports.append(report)

            print(f"从新浪财经获取 {len(reports)} 篇相关研报")
            return reports

        except Exception as e:
            print(f"获取新浪财经研报失败: {str(e)}")
            return []

    def format_reports(self, reports: List[Dict]) -> str:
        """
        格式化研报输出

        Args:
            reports: 研报列表

        Returns:
            格式化的研报文本
        """
        if not reports:
            return "未找到相关研报"

        output = []
        output.append("=" * 80)
        output.append(f"研报汇总 | 共 {len(reports)} 篇")
        output.append("=" * 80)
        output.append("")

        for i, report in enumerate(reports, 1):
            output.append(f"【{i}】{report.get('title', '')}")
            output.append(f"机构: {report.get('institution', '')}")
            output.append(f"日期: {report.get('date', '')}")
            if report.get('rating'):
                output.append(f"评级: {report.get('rating')}")
            if report.get('summary'):
                output.append(f"摘要: {report.get('summary', '')}")
            output.append(f"链接: {report.get('url', '')}")
            output.append("-" * 80)

        return "\n".join(output)

    def save_reports(self, reports: List[Dict], output_file: str):
        """
        保存研报到文件

        Args:
            reports: 研报列表
            output_file: 输出文件路径
        """
        formatted_text = self.format_reports(reports)

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            print(f"研报已保存到: {output_file}")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='爬取行业研报')
    parser.add_argument('--industry', type=str, required=True, help='行业名称')
    parser.add_argument('--days', type=int, default=30, help='获取近N天的研报，默认30天')
    parser.add_argument('--output', type=str, help='输出文件路径（可选）')
    parser.add_argument('--source', type=str, default='eastmoney', choices=['eastmoney', 'sina', 'all'], help='数据源选择')

    args = parser.parse_args()

    fetcher = ReportFetcher()
    all_reports = []

    # 根据选择的数据源获取研报
    if args.source in ['eastmoney', 'all']:
        print(f"\n{'='*60}")
        print(f"从东方财富获取研报...")
        print(f"{'='*60}")
        reports = fetcher.fetch_eastmoney_reports(args.industry, args.days)
        all_reports.extend(reports)
        time.sleep(2)  # 避免请求过快

    if args.source in ['sina', 'all']:
        print(f"\n{'='*60}")
        print(f"从新浪财经获取研报...")
        print(f"{'='*60}")
        reports = fetcher.fetch_sina_reports(args.industry, args.days)
        all_reports.extend(reports)

    # 输出结果
    if all_reports:
        formatted_output = fetcher.format_reports(all_reports)
        print("\n" + formatted_output)

        # 保存到文件
        if args.output:
            fetcher.save_reports(all_reports, args.output)
    else:
        print(f"\n未找到关于 '{args.industry}' 的相关研报")
        print("建议:")
        print("1. 尝试使用更通用的行业名称（如 '汽车' 而非 '新能源汽车'）")
        print("2. 增加时间范围（使用 --days 参数）")
        print("3. 尝试其他数据源（使用 --source sina）")


if __name__ == '__main__':
    main()
