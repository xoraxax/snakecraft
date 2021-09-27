import configparser
import importlib
import os
import sys
import traceback

import click

from .core import reset_model, write_json
from .utils import assign_config


def load_ini(ini_path):
    base_path = os.path.dirname(os.path.abspath(ini_path))
    config = configparser.ConfigParser(allow_no_value=True, delimiters="=")
    config.read(ini_path)
    return {
        os.path.join(base_path, section): (
            {
                key: config[section][key]
                for key in config[section]
                if config[section][key] is not None
            },
            [key for key in config[section] if config[section][key] is None],
        )
        for section in config.sections()
    }


def clean_sys_modules(old_sys_modules):
    too_much = sys.modules.keys() - old_sys_modules
    for mod_name in too_much:
        del sys.modules[mod_name]
    importlib.invalidate_caches()


def error(msg):
    click.echo(click.style(msg, fg="red", bg="black"))


@click.command()
@click.option(
    "--output-prefix",
    default="./config",
    help="Destination of the code generation, file extension .tf.json will be appended.",
)
@click.option(
    "--ini-path",
    default="snakecraft.ini",
    help="File path of the snakecraft.ini that is used.",
)
@click.argument("input_module", nargs=-1)
def main(output_prefix, input_module, ini_path):
    """SnakeCraft Python to Terraform transpilation"""
    if os.path.exists(ini_path):
        click.echo("Loading %r" % (ini_path,))
        jobs = load_ini(ini_path)
    else:
        if not input_module:
            click.echo("Could not find snakecraft.ini and input modules specified!")
            raise SystemExit(1)
        jobs = {output_prefix: input_module}

    for output_path, (env, filenames) in sorted(jobs.items()):
        sys_modules = set(sys.modules)
        output_path = output_path + ".tf.json"
        click.echo("Generating %r" % (output_path,))
        assign_config(env)

        for attribute_path in filenames:
            try:
                module_name, attribute_name = attribute_path.split(":")
            except ValueError:
                error(
                    "Invalid module/callable specification: %r, should be module:callable_name."
                    % (attribute_path,)
                )
                continue
            try:
                mod = importlib.import_module(module_name)
            except:
                error("Error while evaluating module %r:" % (module_name,))
                traceback.print_exc()
                continue
            attribute = getattr(mod, attribute_name, None)
            if attribute is None:
                error("Attribute %r not found in module %r" % (attribute_name, module_name))
                continue
            try:
                attribute()
            except:
                error("Error while calling function %r:" % (attribute_name,))
                traceback.print_exc()
                continue

        with open(output_path, "w") as output_file_obj:
            write_json(output_file_obj)
        reset_model()
        clean_sys_modules(sys_modules)


if __name__ == "__main__":
    main()
