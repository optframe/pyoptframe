load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "optframe_lib",
    srcs = ["optframe/optframe_lib.cpp"],
    hdrs = ["optframe/optframe_lib.h"],
    linkstatic=False,
    deps = ["@OptFrame//include:OptFCore"]
)
