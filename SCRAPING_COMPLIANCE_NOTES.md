# Scraping Compliance Notes

Saved on: June 6, 2026

目前项目只实现了 **Eventbrite 和 Luma 两个来源**。用户提到的另外三个网站尚未指定，因此暂时无法判断它们是否允许抓取。

## 是否允许抓取

- **Eventbrite：不允许直接网页抓取。**
  Eventbrite 服务条款第 13 节明确禁止使用 scraper、crawler 或其他自动化方式从网站提取数据。继续使用当前 HTML 抓取器会违反其服务条款。更合适的方式是申请并使用 Eventbrite 官方 API，并遵守其 API 条款。

- **Luma：网页抓取存在较高合规风险。**
  Luma 条款要求只能通过其“公开支持的接口”访问服务，并限制复制、重新发布和传播网站内容。HTML 抓取以及未公开支持的接口都不应直接用于正式产品。建议使用 Luma 官方 API、日历订阅、RSS/ICS，或者取得书面许可。

- `robots.txt` 只表达网站给机器人的访问偏好，**不等于法律许可**。即使 robots.txt 允许访问，也仍需遵守服务条款、版权、隐私和当地法律。

## 目前使用的策略

当前代码采用的是低频、公开页面抓取：

- APScheduler 每天凌晨 2 点运行一次。
- 使用 `httpx` 请求公开搜索页面，不登录、不绕过验证码、不规避访问限制。
- 按 AI、blockchain、Web3 等关键词搜索。
- 使用 BeautifulSoup 提取活动标题、链接和时间。
- 使用来源和活动 ID 去重，然后写入 SQLite。
- 仅保存公开活动信息，不抓取用户邮箱、参与者名单等个人数据。

但当前实现还有合规缺口：

- 没有自动检查和遵守 `robots.txt`。
- 没有完整的请求限速、退避和来源停用机制。
- Eventbrite 当前使用 HTML 抓取，违反其明确条款。
- Luma 原搜索地址已经失效；发现接口仅完成测试，尚未写入项目代码。

## 建议调整为合规优先策略

1. 停用 Eventbrite HTML 抓取，改用官方 API 或获得书面许可。
2. Luma 仅使用官方支持的 API、RSS/ICS 或授权接口。
3. 每个来源建立合规配置：条款链接、API 凭证、请求频率、允许保存的字段。
4. 只保存活动名称、时间、地点、来源链接等必要元数据，不复制图片和完整描述。
5. 添加限速、来源失败隔离、robots.txt 检查、来源署名和数据删除机制。
6. 在确定另外三个网站后，逐一检查其条款和 API。

这不是正式法律意见。如果项目将公开运营或商业化，建议让熟悉加拿大及美国互联网、版权和隐私法律的律师审核。

## Sources

- Eventbrite 服务条款：https://www.eventbrite.com/help/en-us/articles/251210/eventbrite-terms-of-service/
- Eventbrite API 条款：https://www.eventbrite.com/help/en-us/articles/833731/eventbrite-api-terms-of-use/
- Luma 使用条款：https://luma.com/terms
