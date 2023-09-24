from typing import NewType

Character = NewType("Character", str)
SimplifiedCharacter = NewType("SimplifiedCharacter", Character)
TraditionalCharacter = NewType("TraditionalCharacter", Character)
Definition = NewType("Definition", str)
PinyinToneMarks = NewType("PinyinToneMarks", str)
PinyinNoToneMarks = NewType("PinyinNoToneMarks", str)
PinyinToneNumbers = NewType("PinyinToneNumbers", str)
PinyinNoSpacesNoToneMarks = NewType("PinyinNoSpacesNoToneMarks", str)
Classifier = NewType("Classifier", str)
Frequency = NewType("Frequency", int)
