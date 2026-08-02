from unasync import Rule
from tokenize_rt import src_to_tokens



class PyHiveUnasyncRule(Rule):

    ATTRIBUTE_REPLACEMENTS = {
        ("asyncio", "current_task"): {
            "replacement": (None, "current_thread"),
            "import": ("threading", "current_thread"),
        },
        ("asyncio", "Task"): {
            "replacement": (None, "Thread"),
            "import": ("threading", "Thread"),
        },
        ("asyncio", "sleep"): {
            "replacement": ("time", "sleep"),
        },
        ("asyncio", "TimeoutError"): {
            "replacement": (None, "TimeoutError"),
        }
    }

    def _postprocess_tokens(self, tokens):
        # temporary bypass of function while testing move of code to unasync
        return tokens

    def _old_impl_of_postprocess_tokens(self, tokens):
        required_imports = set()
        seen_imports = set()
        tokens = list(tokens)
        result = []

        i = 0

        while i < len(tokens):

            #
            # Look for import
            #
            if (
                i + 1 < len(tokens)
                and tokens[i].src == "import"
                and tokens[i + 1].name == "NAME"
            ):
                seen_imports.add(("import", tokens[i + 1].src))
            #
            # Scan forward for multiple imports after from
            #
            if (
                i + 2 < len(tokens)
                and tokens[i].src == "from"
                and tokens[i + 1].name == "NAME"
                and tokens[i + 2].src == "import"
            ):
                module = tokens[i + 1].src

                j = i + 3

                while j < len(tokens):

                    #
                    # End of this import statement?
                    #
                    if tokens[j].name == "NEWLINE":
                        break

                    #
                    # Imported name?
                    #
                    if tokens[j].name == "NAME":
                        seen_imports.add(("from", module, tokens[j].src))

                    j += 1
            #
            # Look for NAME . NAME
            #
            if (
                i + 2 < len(tokens)
                and tokens[i].name == "NAME"
                and tokens[i + 1].src == "."
                and tokens[i + 2].name == "NAME"
            ):

                key = (tokens[i].src, tokens[i + 2].src)

                if key in self.ATTRIBUTE_REPLACEMENTS:
                    rule = self.ATTRIBUTE_REPLACEMENTS[key]

                    module, attribute = rule["replacement"]

                    if "import" in rule:
                        required_imports.add(rule["import"])

                    if module is not None:
                        result.append(tokens[i]._replace(src=module))
                        result.append(tokens[i + 1])
                        result.append(tokens[i + 2]._replace(src=attribute))
                    else:
                        result.append(tokens[i + 2]._replace(src=attribute))

                    i += 3
                    continue

            result.append(tokens[i])
            i += 1

            missing_imports = []
            for module, name in required_imports:
                if ("from", module, name) not in seen_imports:
                    missing_imports.append((module, name))

        import_text = ""

        for module, name in sorted(missing_imports):
            import_text += f"from {module} import {name}\n"
            
        import_tokens = list(src_to_tokens(import_text))

        #
        # Build the missing imports
        #
        import_text = ""

        for module, name in sorted(missing_imports):
            import_text += f"from {module} import {name}\n"

        new_tokens = list(src_to_tokens(import_text))

        insert_at = _find_import_insertion_point(result, tokens)
        #
        # Insert them
        #
        result[insert_at:insert_at] = new_tokens

        return result

def _find_import_insertion_point(self, tokens):

    i = 0

    #
    # Skip initial comments / blank lines
    #
    while i < len(tokens):
        if tokens[i].name in ("NL", "COMMENT"):
            i += 1
        else:
            break

    #
    # Skip module docstring
    #
    if i < len(tokens) and tokens[i].name == "STRING":

        while i < len(tokens):
            if tokens[i].name == "NEWLINE":
                i += 1
                break
            i += 1

    #
    # Skip blank lines after docstring
    #
    while i < len(tokens):
        if tokens[i].name in ("NL", "COMMENT"):
            i += 1
        else:
            break

    insert_at = i

    # now scan over import statements
    while i < len(tokens):
        #
        # import ...
        #
        if tokens[i].src == "import":

            while tokens[i].name != "NEWLINE":
                i += 1
            i += 1
            insert_at = i
            continue

        #
        # from ... import ...
        #
        if tokens[i].src == "from":

            while tokens[i].name != "NEWLINE":
                i += 1
            i += 1
            insert_at = i
            continue

        #
        # Blank line between imports?
        #
        if tokens[i].name == "NL":
            i += 1
            insert_at = i - 1
            continue

        break

    return insert_at
