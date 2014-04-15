from __future__ import print_function, division, absolute_import

from argparse import ArgumentParser


descr = 'Create or extract a "bundle package" (EXPERIMENTAL)'


def configure_parser(sub_parsers):
    p = argparse.ArguemntParser(
        'bundle',
        description="analysis package",
        help="analysis package"
    )
    cxgroup = p.add_mutually_exclusive_group()
    cxgroup.add_argument('-c', "--create",
                         action = "store_true",
                         help = "create bundle")
    cxgroup.add_argument('-x', "--extract",
                         action = "store",
                         help = "extact bundle located at PATH",
                         metavar = "PATH")
    cxgroup.add_argument("--metadump",
                         action = "store",
                         help = "dump metadata of bundle at PATH",
                         metavar = "PATH")

    common.add_parser_prefix(p)
    common.add_parser_quiet(p)
    p.add_argument("--bundle-name",
                   action = "store",
                   help = "name of bundle",
                   metavar = 'NAME',
                   )
    p.add_argument("--data-path",
                   action = "store",
                   help = "path to data to be included in bundle",
                   metavar = "PATH",
                   )
    p.add_argument("--extra-meta",
                   action = "store",
                   help = "path to json file with additional meta-data no",
                   metavar = "PATH",
                   )
    p.add_argument("--no-env",
                   action = "store_true",
                   help = "no environment",
                   )
    common.add_parser_json(p)
    p.set_defaults(func=execute)


def execute(args, parser):
    import sys
    import json

    import conda.bundle as bundle
    from conda.fetch import TmpDownload


    if not (args.create or args.extract or args.metadump):
        sys.exit("""Error:
    either one of the following options is required:
       -c/--create  -x/--extract  --metadump
    (see -h for more details)""")
    prefix = common.get_prefix(args)
    if args.no_env:
        prefix = None

    if args.create:
        if args.extra_meta:
            with open(args.extra_meta) as fi:
                extra = json.load(fi)
            if not isinstance(extra, dict):
                sys.exit('Error: no dictionary in: %s' % args.extra_meta)
        else:
            extra = None

        bundle.warn = []
        out_path = bundle.create_bundle(prefix, args.data_path,
                                        args.bundle_name, extra)
        if args.json:
            d = dict(path=out_path, warnings=bundle.warn)
            json.dump(d, sys.stdout, indent=2, sort_keys=True)
        else:
            print(out_path)


    if args.extract:
        if args.extra_meta:
            sys.exit("""\
Error: -x/--extract does not allow --extra-meta""")

        with TmpDownload(args.extract, verbose=not args.quiet) as path:
            bundle.clone_bundle(path, prefix, args.bundle_name, 
                                data_path=args.data_path)


    if args.metadump:
        import tarfile

        with TmpDownload(args.metadump, verbose=not args.quiet) as path:
            try:
                t = tarfile.open(path, 'r:*')
                f = t.extractfile('info/index.json')
                sys.stdout.write(f.read())
                sys.stdout.write('\n')
            except IOError:
                sys.exit("Error: no such file: %s" % path)
            except tarfile.ReadError:
                sys.exit("Error: bad tar archive: %s" % path)
            except KeyError:
                sys.exit("Error: no archive '%s' in: %s" % (bundle.BMJ, path))
            t.close()
