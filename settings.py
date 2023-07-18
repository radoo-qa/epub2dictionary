def choose_chapter(contents_url):
    print('All the chapters are listed bellow. Which one do you want to translate? Input the title of the chapter.')

    for chapter_name in contents_url.keys():
        print(f"{chapter_name}")

    output = input()

    if output in contents_url:
        return output
    else:
        raise ValueError('Incorrect chapter name')


def set_previous_words(chapters2translate, contents_url):
    if chapters2translate != list(contents_url.keys())[0]:
        output = input('Should the dictionary include words that have already appeared in previous chapters? Yes/No.')

        if output.casefold() == 'yes':
            return True
        elif output.casefold() == 'no':
            return False
        else:
            raise ValueError('Incorrect - input yes or no')
    else:
        return False


def chapters_to_parse(chapters2translate, contents_url, previous_words):
    if not previous_words:
        return {chapters2translate: contents_url[chapters2translate]}

    else:
        output = {}
        for chapter_name, chapter_link in contents_url.items():
            output[chapter_name] = chapter_link
            if chapter_name == chapters2translate:
                break
        return output

