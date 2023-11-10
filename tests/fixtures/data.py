from app.domain.vocabulary import character, common, word


def sample_words() -> list[word.WordSchema]:
    return [
        word.WordSchema(
            simplified=word.SimplifiedWord(word.Word("鸦雀无声")),
            traditional=word.TraditionalWord(word.Word("鴉雀無聲")),
            pinyin_num=common.PinyinToneNumbers("ya1 que4 wu2 sheng1"),
            pinyin_accent=common.PinyinToneMarks("yā què wú shēng"),
            pinyin_clean=common.PinyinNoToneMarks("ya que wu sheng"),
            pinyin_no_spaces=common.PinyinNoSpacesNoToneMarks("yaquewusheng"),
            also_written=word.AlsoWritten(""),
            also_pronounced=word.AlsoPronounced(""),
            classifiers=word.Classifiers(""),
            definitions=common.Definition(
                (
                    "lit. crow and peacock make no sound; absolute silence (idiom); "
                    "not a single voice can be heard; absolute silence"
                )
            ),
            frequency=common.Frequency(189),
        )
    ]


def sample_characters() -> list[character.CharacterSchema]:
    return [
        character.CharacterSchema(
            character=common.Character("声"),
            definition=common.Definition("sound, noise; voice, tone, music"),
            pinyin=common.PinyinToneMarks("shēng"),
            decomposition=character.Decomposition("⿱士？"),
            etymology=character.Etymology(
                hint="Simplified form of 聲; see that character for the etymology",
                type="ideographic",
            ),
            radical=character.Radical("士"),
            matches=character.Matches("[[0], [0], [0], None, None, None, None]"),
            frequency=common.Frequency(31194),
        ),
        character.CharacterSchema(
            character=common.Character("雀"),
            definition=common.Definition("sparrow"),
            pinyin=common.PinyinToneMarks("què"),
            decomposition=character.Decomposition("⿱小隹"),
            etymology=character.Etymology(hint="A small 小 bird 隹", type="ideographic"),
            radical=character.Radical("隹"),
            matches=character.Matches("[[0], [0], [0], [1], [1], [1], [1], [1], [1], [1], [1]]"),
            frequency=common.Frequency(650),
        ),
        character.CharacterSchema(
            character=common.Character("无"),
            definition=common.Definition("no, not; lacking, -less"),
            pinyin=common.PinyinToneMarks("wú"),
            decomposition=character.Decomposition("⿱一尢"),
            etymology=None,
            radical=character.Radical("无"),
            matches=character.Matches("[[0], [1], [1], [1]]"),
            frequency=common.Frequency(32945),
        ),
        character.CharacterSchema(
            character=common.Character("鸦"),
            definition=common.Definition("crow; Corvus species (various)"),
            pinyin=common.PinyinToneMarks("yā"),
            decomposition=character.Decomposition("⿰牙鸟"),
            etymology=character.Etymology(
                semantic="鸟",
                phonetic="牙",
                hint="bird",
                type="pictophonetic",
            ),
            radical=character.Radical("鸟"),
            matches=character.Matches("[[0], [0], [0], [0], [1], [1], [1], [1], [1]]"),
            frequency=common.Frequency(321),
        ),
    ]
