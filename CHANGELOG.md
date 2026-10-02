# Changelog

## [1.1.0](https://github.com/jose-fernandez/telegram-monitor/compare/telegram-monitor-v1.0.0...telegram-monitor-v1.1.0) (2026-10-02)


### Features

* let users choose the time zone of the logs with TZ ([cf42891](https://github.com/jose-fernandez/telegram-monitor/commit/cf428914c99d6b2f05feaa74a2bc20dd7178330c))
* let users choose the time zone of the logs with TZ ([c73fe90](https://github.com/jose-fernandez/telegram-monitor/commit/c73fe90df58101ad904a0f7507ba905cda5b0c26))

## 1.0.0 (2026-10-02)


### Features

* Docker image published to ghcr.io, with all state kept in one data folder ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* English and Spanish messages ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* manage keywords, channels and language by sending commands to Saved Messages ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* monitor Telegram channels from your own account and alert on keywords through your own bot ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* never lose an alert: long posts are split, alerts over the rate limit wait their turn, and temporary failures are retried ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* visual setup window (main_gui.py) for logging in and managing keywords and channels ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))


### Bug Fixes

* channel text with stray Markdown characters no longer makes alerts fail ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* INFO logs now reach the console and docker logs ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))
* setup window stores its login in the data folder, where the bot looks for it ([05abd18](https://github.com/jose-fernandez/telegram-monitor/commit/05abd182ddef810c79f87133ec8c1d7010ae63e7))


### Continuous Integration

* publish versioned releases with release-please ([2c1995e](https://github.com/jose-fernandez/telegram-monitor/commit/2c1995eb32dad98852de175af5f8fc49593891d1))
