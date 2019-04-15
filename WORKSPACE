load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "build_stack_rules_proto",
    sha256 = "5474d1b83e24ec1a6db371033a27ff7aff412f2b23abba86fedd902330b61ee6",
    strip_prefix = "rules_proto-91cbae9bd71a9c51406014b8b3c931652fb6e660",
    urls = ["https://github.com/stackb/rules_proto/archive/91cbae9bd71a9c51406014b8b3c931652fb6e660.tar.gz"],
)

load("@build_stack_rules_proto//python:deps.bzl", "python_grpc_library")

python_grpc_library()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@io_bazel_rules_python//python:pip.bzl", "pip_import", "pip_repositories")

pip_repositories()

pip_import(
    name = "protobuf_py_deps",
    requirements = "@build_stack_rules_proto//python/requirements:protobuf.txt",
)

load("@protobuf_py_deps//:requirements.bzl", protobuf_pip_install = "pip_install")

protobuf_pip_install()

pip_import(
    name = "grpc_py_deps",
    requirements = "@build_stack_rules_proto//python:requirements.txt",
)

load("@grpc_py_deps//:requirements.bzl", grpc_pip_install = "pip_install")

grpc_pip_install()

git_repository(
    name = "trillian",
    branch = "bazel_fun",
    remote = "https://github.com/mhutchinson/trillian.git",
)

http_archive(
    name = "googleapi",
    url = "https://github.com/googleapis/googleapis/archive/master.zip",
    strip_prefix = "googleapis-master",
)

# TODO(mhutchinson): Determine why Go libraries are required
http_archive(
    name = "io_bazel_rules_go",
    strip_prefix = "rules_go-7d17d496a6b32f6a573c6c22e29c58204eddf3d4",
    urls = ["https://github.com/bazelbuild/rules_go/archive/7d17d496a6b32f6a573c6c22e29c58204eddf3d4.zip"],
)
