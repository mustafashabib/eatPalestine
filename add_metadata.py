#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging, os, glob, re
from pprint import pprint

def get_alphanumeric_part(s):
      return s[find_first_alphanumeric(s):]

def find_first_alphanumeric(s):
      i = 0
      while not s[i].isalpha() and not str(s[i]).isdigit():
            i += 1

      return i

def add_metadata(path):
      for filepath in glob.glob(os.path.join(path, '*.md')):
            try:
              logging.debug('Attempting to add metadata to %s', filepath)
              add_metadata_to_file(filepath)
            except Exception as e:
              logging.exception('could not add metadata to %s, %s', filepath, e)

            logging.debug('====\n')

def add_metadata_to_file(filepath):
      with open(filepath, 'r+') as f:
        content = f.read()

        # get servings
        SERVINGS_HEADER = '# Makes '
        SERVINGS_HEADER_LEN = len(SERVINGS_HEADER)

        start_servings = content.index(SERVINGS_HEADER) + SERVINGS_HEADER_LEN
        end_servings = content.index('\n', start_servings)
        servings = content[start_servings:end_servings]
        logging.debug('GOT SERVINGS\n\t%s', servings)

        # get ingredients
        ingredients_start = end_servings
        ingredients_end = content.index('#### Recipe')
        ingredients_block = content[ingredients_start:ingredients_end]
        ingredients_lines = ingredients_block.split('\n')
        ingredients_lines = [x for x in ingredients_lines if x.strip() != '']
        final_ingredients = []
        for i in range(0, len(ingredients_lines), 2):
              name = get_alphanumeric_part(ingredients_lines[i])
              amount = get_alphanumeric_part(ingredients_lines[i+1])
              final_ingredients.append('{} ({})'.format(name, amount))
        logging.debug('GOT INGREDIENTS\n\t%s', final_ingredients)

        # get instructions
        instructions_block = content[content.index('1.', ingredients_end):]
        instructions_lines = instructions_block.split('\n')
        final_instructions = [x for x in instructions_lines if x.strip() != '']
        logging.debug('GOT INSTRUCTIONS\n\t%s', final_instructions)

        # get metadata
        METADATA_START = 0
        METADATA_LEN = 3
        metadata_end = content.index('---', METADATA_START+METADATA_LEN) + METADATA_LEN
        metadata_block = content[METADATA_START:metadata_end]
        logging.debug("GOT METADATA\n\n%s", metadata_block)
        content = content[metadata_end:]
        metadata_lines = metadata_block.split('\n')
        metadata_lines.pop(0) # remove first
        metadata_lines.pop() # remove last
        metadata_lines.append('servings: %s' % servings)
        metadata_lines.append('ingredients: %s' % str(final_ingredients))
        metadata_lines.append('instructions: %s' % str(final_instructions))
        metadata_lines.append('---')
        metadata_lines.insert(0, '---')
        logging.debug('NEW METADATA\n\n%s', '\n'.join(metadata_lines))

        content = '\n'.join(metadata_lines) + content
        f.seek(0)
        f.write(content)
        f.truncate()



# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  path = args.argument
  add_metadata(path)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser(
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
  # TODO Specify your real parameters here.
  parser.add_argument(
                      "argument",
                      help = "pass ARG to the program",
                      metavar = "ARG")
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()

  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

  main(args, loglevel)
