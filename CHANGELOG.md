## [4.0.4](https://github.com/alexschimpf/rest-api-tester/compare/v4.0.3...v4.0.4) (2024-03-19)


### Bug Fixes

* Fixed content-type check in default_verifier ([fb154dc](https://github.com/alexschimpf/rest-api-tester/commit/fb154dc89c512eb60b92f955847bd326d6669dfc))

## [4.0.3](https://github.com/alexschimpf/rest-api-tester/compare/v4.0.2...v4.0.3) (2024-03-15)

## [4.0.2](https://github.com/alexschimpf/rest-api-tester/compare/v4.0.1...v4.0.2) (2024-03-14)


### Bug Fixes

* Fixed update_scenarios_on_fail handling of content-type ([38641ea](https://github.com/alexschimpf/rest-api-tester/commit/38641ea49eef85fa1e0f78a88322cca9472742ed))

## [4.0.1](https://github.com/alexschimpf/rest-api-tester/compare/v4.0.0...v4.0.1) (2024-03-14)


### Bug Fixes

* Proper parser handling of json modifiers with missing request/response ([64191a9](https://github.com/alexschimpf/rest-api-tester/commit/64191a950ac9bed6d424db61c3be58b193606b97))

## [4.0.0](https://github.com/alexschimpf/rest-api-tester/compare/v3.0.0...v4.0.0) (2024-03-14)


### Breaking Changes

* Changed how update_scenarios_on_fail writes placeholder text ([59703f9](https://github.com/alexschimpf/rest-api-tester/commit/59703f948a0a3ddd7fbdd037d5108e9f292d5ede))

## [3.0.0](https://github.com/alexschimpf/rest-api-tester/compare/v2.0.4...v3.0.0) (2024-01-08)


### Breaking Changes

* Added ability to add a description for each test case. Now allowing a list of test_data_modifiers. Added `response_header_modifiers` and `request_header_modifiers` params. Made `update_scenarios_on_fail` a proper instance var of TestCase. Simplified package imports. Fixed `test_data_modifier` param  description. Fixed `excluded_response_paths` bug where excluded response fields were not being properly applied to expected response. Added `update_scenarios_on_fail_options` param. ([8841538](https://github.com/alexschimpf/rest-api-tester/commit/88415387f9313dbe67854e8de921be2ede388dcf))

## [2.0.4](https://github.com/alexschimpf/rest-api-tester/compare/v2.0.3...v2.0.4) (2023-09-22)


### Bug Fixes

* Fixed handling and formatting of empty requests and responses ([4e08d22](https://github.com/alexschimpf/rest-api-tester/commit/4e08d229e4d853994cb0c5b2763ad1c6b78eedc5))

## [2.0.3](https://github.com/alexschimpf/rest-api-tester/compare/v2.0.2...v2.0.3) (2023-09-20)


### Bug Fixes

* Fixed issue with update_scenarios_on_fail initialization ([a56af95](https://github.com/alexschimpf/rest-api-tester/commit/a56af952e4310bf6ba689c4f005c8c3389668b0e))
* Fixed the behavior of update_scenarios_on_fail when handling JSON responses ([dc357c0](https://github.com/alexschimpf/rest-api-tester/commit/dc357c0b66d07b7a5aa7bff60304227782aeea75))

## [2.0.2](https://github.com/alexschimpf/rest-api-tester/compare/v2.0.1...v2.0.2) (2023-09-20)


### Bug Fixes

* Fixed package build error ([79e5d5f](https://github.com/alexschimpf/rest-api-tester/commit/79e5d5f4980afab60ae2745799621b16fb8bf65a))

## [2.0.1](https://github.com/alexschimpf/rest-api-tester/compare/v2.0.0...v2.0.1) (2023-09-12)


### Bug Fixes

* Removed requests from requirements.txt ([ed697bc](https://github.com/alexschimpf/rest-api-tester/commit/ed697bc17d352c359e6585872ba3dca98ba30d31))

# [2.0.0](https://github.com/alexschimpf/rest-api-tester/compare/v1.0.0...v2.0.0) (2023-09-12)
