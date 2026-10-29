# Agent 工作约定

本文件所在目录是项目根目录。后端在 `backend/`，网页资源在 `backend/static/`；所有命令从项目根目录执行。

## 用户要求启动时

1. **先确认是否已运行。** 读取 `config.local.json` 中的端口和路径，不输出整个私有配置。macOS 可执行：

   ```sh
   launchctl print "gui/$(id -u)/com.codex.dingtalk-ears"
   ```

   同时检查配置端口的 HTTP 响应。默认端口示例：

   ```sh
   curl --fail --silent --show-error --output /dev/null http://127.0.0.1:8766/
   ```

   若实际服务和页面正常，复用已有实例并给出面板链接。已有服务异常或端口被占用时，先检查进程、状态和日志，再决定恢复方式，避免重复启动。

2. **确认配置和依赖。** 检查 `python3`、`dws`、`codex` 可执行。优先沿用已安装启动项中的 Python 与环境；使用 nvm 时确认 PATH 中有 Node。缺少 CLI、配置或登录时，先读 [README](README.md) 的安装步骤；字段、OpenID、权限或迁移问题读 [安装配置与启动](docs/安装配置与启动.md)。

   `init` 只创建模板，不会自动读取 DWS 身份。只有配置缺失时才执行：

   ```sh
   python3 -m backend init --output config.local.json
   ```

   从真实 CLI 返回值核对账号、本人 OpenID 和群 ID。保留已有配置和登录态；新用户的数据库会由程序自动创建。

3. **运行诊断。** 没有正在运行的实例时执行：

   ```sh
   python3 -m backend --config config.local.json doctor
   ```

   处理阻断错误并说明 warning。登录失败时按 README 引导本人完成对应 CLI 授权；不复制他人的认证目录。已有正常实例导致的端口占用不需要重启处理。

4. **按运行方式启动。** 前台运行：

   ```sh
   python3 -m backend --config config.local.json run
   ```

   用户要求持续后台运行时，在 macOS、前台实例退出后安装登录启动项：

   ```sh
   python3 -m backend --config config.local.json service --install
   ```

   已安装但尚未加载时复用安装项：

   ```sh
   launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.codex.dingtalk-ears.plist"
   ```

   新生成的 `.plist` 文件默认不覆盖已有文件；需要重新生成时用 `--output` 指定新的 `.plist` 路径。Linux 使用前台运行或明确配置的用户服务。

5. **验证后再报告已启动。** 确认进程存活、配置端口 HTTP 可访问、输出目录中的 `运行状态.json` 持续更新，并核对监听和 App Server 状态。`ready` 只表示订阅就绪，不能据此宣称真实群消息已投递；`degraded` 等异常要如实说明。报告实际面板地址、运行方式和剩余问题。

## 停止与数据

- 前台用 Ctrl+C 正常停止；macOS 后台用 `launchctl bootout "gui/$(id -u)/com.codex.dingtalk-ears"`。只操作本项目实例，避免广泛终止 Python、Node 或其他 Codex 进程。
- 数据库、日志与会话位于配置的 `paths.state_dir`；运行状态与摘要位于 `paths.output_dir`。启动时保留这些数据。
- `run --adopt-state` 仅用于已备份且核对为同一账号、同一群的旧数据库；普通新用户无需使用。身份不匹配时使用独立目录，不删除身份标记绕过检查。
- 启动验证仅做读取检查，不自动发送钉钉消息或创建待办。所有回复及待办仍需本人确认，不接入 OA 审批。

## 修改代码时

- 通用提示词只在 `backend/prompts.py` 管理，输出契约在 `backend/ai_contract.py`；个人称呼仅作为私有上下文数据，不写入通用指令。
- 配置、凭据、数据库、日志、摘要和截图不进入分享包。分享由 `backend/distribution.py` 的白名单控制。
- 开发环境与统一检查见 README。修改运行逻辑后执行 `python scripts/check.py`；用 `python3 -m unittest discover -s tests -v` 检查运行兼容性。仅修改文档时检查命令与链接即可。
