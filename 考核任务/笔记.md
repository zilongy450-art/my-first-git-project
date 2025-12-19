HTTP & HTTPS 基本概念
HTTP 是什么：
层次：应用层协议，基于 TCP。
场景：典型 B/S 架构（浏览器/服务器）。
特点：
无状态：服务器不记得上一次请求的状态。
一次请求 = 客户端发 HTTP 请求 → 服务器回 HTTP 响应。

 面试常问点：HTTP 是什么？工作在哪一层？是否有状态？

HTTPS 是什么：
HTTPS = HTTP + SSL/TLS，加密版本的 HTTP。
核心三个能力：
1. 机密性：传输内容加密。
2. 身份认证：验证网站身份（防钓鱼）。
3. 完整性：防篡改。
简化握手流程：
  1. 客户端发起 HTTPS 请求。
  2. 服务器返回数字证书（含公钥）。
  3. 客户端验证证书 → 生成随机密钥 → 用公钥加密发给服务器。
  4. 服务器用私钥解密拿到随机密钥。
  5. 后续用这个随机密钥做对称加密通信。

HTTP vs HTTPS（面试必问）

对比要点：

安全性：
HTTP：明文传输，不安全。
HTTPS：加密传输，更安全。
端口：
HTTP 默认 80
HTTPS 默认 443
证书：
HTTPS 需要 CA 颁发的证书（通常收费）。
性能：
HTTPS 有加密/解密开销，相比慢一点。
SEO：搜索引擎偏向 HTTPS。

面试一句话回答模板：
“HTTPS = HTTP + SSL/TLS，通过证书+加解密实现机密性、身份认证和完整性，默认 443 端口，比 HTTP 安全，但有一定性能开销。”


HTTP 请求结构

三大部分

1. 请求行：
格式：方法 URI 协议/版本，例如：`GET /sample.jsp HTTP/1.1`
2. 请求头：描述客户端环境、请求参数的一些元信息。
3. 请求体：真正要发的数据（POST、PUT 等时常见）。

常见请求方法 & 特性

重点方法及特性：

| 方法      | 特点                 | 典型场景     |
| ------- | ------------------ | -------- |
| GET     | 安全、幂等，参数在 URL 中    | 查询/获取资源  |
| POST    | 不安全、不幂等，参数在 body 中 | 新增/提交表单  |
| PUT     | 幂等，更新资源（整体替换）      | 覆盖更新某资源  |
| DELETE  | 幂等，删除资源            | 删除指定资源   |
| PATCH   | 不幂等，部分更新           | 只改一部分字段  |
| HEAD    | 只要响应头，不要响应体        | 探测资源、做监控 |
| OPTIONS | 查看服务器支持哪些方法        | 跨域预检等    |

幂等：多次调用结果一样（GET/PUT/DELETE 幂等，POST/PATCH 通常不幂等）。

常见请求头

典型字段：

`Host`：服务器域名
`User-Agent`：客户端信息
`Accept` / `Accept-Language` / `Accept-Encoding`
`Content-Type` / `Content-Length`
`Authorization`：认证信息（比如 Token）
`Cookie`：携带 Cookie



HTTP 响应结构 & 常见状态码

响应结构

三部分：

1. 状态行：`HTTP/1.1 200 OK`
2. 响应头：描述服务器和响应信息。
3. 响应体：真正返回的数据（HTML / JSON / 图片 / 视频流…）。

常见响应头：

`Server` / `Content-Type` / `Content-Length` / `Content-Encoding`
`Location`（重定向）
`Set-Cookie`
`Cache-Control` / `Last-Modified` / `ETag`

状态码分类 &重点

分类：

1xx：信息
2xx：成功
3xx：重定向
4xx：客户端错误
5xx：服务器错误

常背代码：

200 OK
201 Created
204 No Content
301 Moved Permanently / 302 Found
304 Not Modified
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable


HTTP 各版本差异

HTTP/1.0 vs HTTP/1.1

关键差异：

连接：
1.0：默认短连接，每次请求一个 TCP。
1.1：默认长连接（`Connection: keep-alive`），支持管线化。
缓存：
1.0：`If-Modified-Since`、`Expires`
1.1：增加 `ETag`、`If-None-Match` 等更灵活策略。
带宽优化：
1.1 支持 `Range` 断点续传 → 返回 206。
Host 头：
1.1 要求必须有 `Host`（支持虚拟主机）。
状态码 & 方法：
1.1 增加更多状态码和方法（PUT、DELETE、OPTIONS、TRACE…）。

HTTP/2 关键新特性
总结：
二进制分帧（Binary）：更高效。
多路复用（Multiplexing）：一个 TCP 里并发多个请求，解决队头阻塞。
Header 压缩（HPACK）：减少重复头部传输。
服务端推送（Server Push）：服务器提前推资源。
请求优先级：重要资源优先。

HTTP/3 改进点：
基于 UDP+QUIC，解决 TCP 层面的队头阻塞。
内置加密（QUIC 自带）。
连接迁移（比如 WiFi → 4G 不断线）。
更快握手和更灵活的拥塞控制。



接口（API）基础

API 接口定义 & 例子
本质：软件提供的“对外能力”，别人只关心“怎么调”，不关心内部实现。
比喻：
“货物”= 数据
“总仓库”= 数据库
“店铺”= 网站/App
“中转站”= API（把数据装包给前端/调用者）。

接口分类
按不同维度：
按协议：RESTful、SOAP、GraphQL、RPC…
按开放程度：公开 API / 内部 API / 合作伙伴 API
按服务类型：Web API / OS API / DB API / 硬件 API…

接口设计原则（重点）
RESTful 风格：用 HTTP 方法表达动作，用 URL 表示资源，用状态码表示结果。
版本控制：v1/v2，向后兼容。
安全性：认证（Token、OAuth）、授权。
文档化：清晰的接口文档。
错误处理：统一错误码/错误结构。
限流：防止滥用。
可测试性：方便自动化测试。

扩展：API 优先设计、OpenAPI、API 网关、微服务适配等。


接口表现形式 & GUI
URL 结构拆解
示例：
`http://www.qubaobei.com/ios/cf/dish_list.php?stage_id=1&limit=20&page=1` 
拆成四块：
1. 协议：`http:`
2. 服务器地址（域名）：`//www.qubaobei.com`
3. 路径：`/ios/cf/dish_list.php`
4. 参数：`?stage_id=1&limit=20&page=1`
这个 URL 就可以被称为“食品模块的一个接口地址”。

GUI 的概念
GUI = 图形用户界面，图形方式（窗口、按钮）和用户交互。
对比：
GUI（Windows） vs CLI（命令行，像 DOS）。

接口传递数据方式 & GET vs POST
GET特点：
数据在 URL 中（查询参数）。
长度有限（URL 一般上限 ~2048 字符）。
能缓存、能被收藏为书签、会保存在浏览器历史。
对用户可见 → 安全性差。
幂等，通常用于查询。
POST特点：
数据在请求体里，长度几乎不限。
不被 URL/历史暴露，相对安全一点。
不能被缓存为普通 GET 书签。
非幂等，一般用于新增/提交。

特别强调：“发送密码或其他敏感信息时绝不要使用 GET！”

 PUT / DELETE / PATCH 简要
PUT：更新/创建，幂等，指定资源位置。
DELETE：删除，幂等。
PATCH：部分更新，通常不幂等。

接口测试：概念、原理、流程
概念 & 本质
测试系统组件之间“交互点”的一种测试（外部系统与系统、内部各子系统之间）。
本质：看 “数据传输+接收”是否正常：
请求：URL + 参数 + 头
响应：文本/文件
对比响应和预期是否一致。

目标
功能正确性
数据完整性/准确性
安全性
性能 & 稳定性
异常情况下的容错能力

原理（流程视角）
简化为：
1. 构造 HTTP 请求（URL、头、参数、body）。
2. 发给服务器。
3. 服务器处理→返回响应。
4. 客户端解析响应 & 做断言。
5. 记录结果。

接口测试完整流程：
1. 拿接口文档（找后端）。
2. 写测试计划。
3. 分析接口：请求参数、请求头（Token、OS、版本）、响应数据结构、错误情况等。
4. 写用例 & 用例评审。
5. 执行用例
手工：Postman/JMeter
自动化：requests + pytest/unittest
6. 分析结果，提 Bug。
7. Bug 修复后回归。

接口测试内容（覆盖哪些方面）

功能逻辑：
验证数据处理是否正确，可查 DB/缓存或其他系统。

异常测试：
参数异常（缺失、类型错误、超范围…）
网络异常、服务器异常（500、服务不可用）
安全异常（未授权、越权）

路径测试：
逻辑分支多、嵌套调用多的接口，需要做路径覆盖：
分析代码分支 → 设计覆盖所有路径的用例。

结构检查：
返回格式 JSON/XML 是否正确。
字段名、字段类型、必填字段、取值范围等。

其他场景：
并发、压力、安全、兼容性等专项场景。

常用接口测试工具

分三类：
1. 商业：
LoadRunner（偏性能）。
SoapUI（曾经很火的 WebService 工具）。
2. 开源：
JMeter：HTTP/Soap/JDBC 等，既能压测又能做接口功能测试。
Postman：REST API 功能测试神器。
3. 扩展插件/现代工具：
浏览器插件 Postman
Insomnia、Swagger UI
K6、Locust 等现代性能 & API 测试框架
Python：requests + pytest / Tavern 等
Java：RestAssured、Spring Boot Test 等

接口文档规范 & 返回结构
接口文档是什么：
前后端（或前端/后端/客户端）协作的“契约”，形式可以是 Word/PDF/HTML/swagger 等。
规范：四大块：
请求方式、URI、请求参数、返回参数
请求方式：POST 新增、PUT 修改、DELETE 删除、GET 查询。
URI 规范：
以 `/a` 开头；
需要登录的接口加 `/a/u`；
后台列表用 `/search` 结尾，前台列表用 `/list` 结尾；
URI 中不用大写字母；多个单词用 `/` 分开。
请求参数（五列）：
字段、说明、类型（String/Number/Object/Array）、备注、是否必填。
返回参数常见 3 种结构：
  1. 只返回成功/失败：`code` + `message`
  2. 附带数据：`code` / `message` / `data`，`data` 是 Object。
  3. 返回列表：`code` / `message` / `data`，`data` 是 Object，里面有
     `page / size / total / totalPage / list`，`list` 是 Array，每项是 object。


接口用例模板 & 设计方法

用例模板核心要素：
文档给的模板关键字段：用例编号、用例标题、模块、优先级、前提条件、请求类型、请求参数、预期结果

常用用例设计方法：
等价类划分（有效/无效等价类）
边界值分析（最小值、最大值、边界前后）
错误推测法（基于经验猜可能出错的地方）
场景法（按业务流程设计：正常流 + 异常流）

接口测试报告

报告要素 & 模板
报告应包含：
1. 系统接口概况(测什么、接口数量等）
2.测试目的与范围
3. 测试环境 & 工具 & 资源
4. 测试记录 & 结果分析（用例通过率、性能结果、问题列表…）
5. 测试结论（接口质量评估、风险、改进建议）


小结：
1. HTTP/HTTPS 基础 & 差异（协议层次、无状态、SSL/TLS、端口等）。
2. HTTP 请求/响应结构（行/头/体，常见头字段，状态码）。
3.HTTP 版本发展（1.0→1.1→2→3，主要改进点）。
4.接口概念/分类/设计原则（RESTful，URI 规范，返回结构 3 种）。
5.数据传输方式 & GET vs POST 差异。
6.接口测试的目标、流程、测试内容（功能/异常/路径/结构/性能/安全）。
7.工具 & 自动化思路（Postman、JMeter、requests+pytest）。
8. 接口文档、用例模板、报告结构（非常适合你现在的面试项目使用）。
