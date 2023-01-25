major = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
melodic_minor = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
harmonic_minor = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
harmonic_major = [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1]
wholetone = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # has only 2 colors (transpositions)
octatonic = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1]  # 3 colors
augmented = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]  # 4 colors

# All proper scales have 12 colors
proper_scales = [major, melodic_minor, harmonic_major, harmonic_minor]
improper_scales = [wholetone, octatonic, augmented]
all_scales = proper_scales + improper_scales


# TODO: There are only 3 operators for proper scales: b3, b6, b7
#       They are all their own onverses


def transpose(x, n):
    return x[-n:] + x[:-n]


def get_transposition(x, y):
    for idx in range(len(x)):
        if transpose(y, idx) == x:
            return idx
    raise ValueError


class BinaryNecklace(tuple):
    def __eq__(self, other):
        for idx in range(len(self)):
            if tuple.__eq__(transpose(self, idx), other):
                return True
        return False

    @property
    def is_harmonic(self):
        indices = [idx for idx, val in enumerate(self) if val == 1]
        for first, third in zip(indices, transpose(indices, -2)):
            if (third - first) % len(self) not in (3, 4):
                return False
        return True


# For now, we will ignore improper scales. Our objects have a shape and a color. Scale families represent shapes.
# Base pitch of the scale represent color (index of its first tone, or its rotation, transposition).
scales = {
    'major': BinaryNecklace(major),
    'melodic_minor': BinaryNecklace(melodic_minor),
    'harmonic_major': BinaryNecklace(harmonic_major),
    'harmonic_minor': BinaryNecklace(harmonic_minor),
    'wholetone': BinaryNecklace(wholetone),
    'augmented': BinaryNecklace(augmented),
    'octatonic': BinaryNecklace(octatonic),
}


class ChromaticNecklace:
    def __init__(self, shape: str, color: int):
        if color not in range(12):
            raise ValueError
        self.name = shape
        self.shape = scales[shape]
        self.state = list(transpose(self.shape, color))
        self.color = color

    def __repr__(self):
        return f'{self.name} ({self.color}): {self.state}'

    def sharpened_state(self, idx):
        state = self.state.copy()
        state[idx], state[(idx + 1) % 12] = 0, 1
        return state

    @staticmethod
    def flipped_state(idx, state):
        new_state = state.copy()
        new_state[idx] = 1 - new_state[idx]
        return new_state

    def is_movable(self, idx):
        if self.state[idx] != 1 or self.state[(idx + 1) % 12] != 0:
            return False
        sharpened = self.sharpened_state(idx)
        is_harmonic = BinaryNecklace(sharpened).is_harmonic
        # try adding or removing a note
        if not is_harmonic:
            for i, v in enumerate(sharpened):
                if i == idx or i == (idx + 1) % 12:
                    continue
                if BinaryNecklace(self.flipped_state(i, sharpened)).is_harmonic:
                    return True
            return False
        return True

    def move(self, idx):
        if not self.is_movable(idx):
            raise ValueError
        sharpened = self.sharpened_state(idx)
        is_harmonic = BinaryNecklace(sharpened).is_harmonic
        # try adding or removing a note
        if not is_harmonic:
            for i, v in enumerate(sharpened):
                if i == idx or i == (idx + 1) % 12:
                    continue
                new_state = self.flipped_state(i, sharpened)
                if BinaryNecklace(new_state).is_harmonic:
                    sharpened = new_state
        sharpened = BinaryNecklace(sharpened)

        for name, shape in scales.items():
            if sharpened == shape:
                new_shape, new_color = name, get_transposition(tuple(sharpened), tuple(shape))
                return ChromaticNecklace(new_shape, new_color)


def main():
    chrome = ChromaticNecklace('harmonic_major', 0)
    print('Initial necklace:')
    print(chrome)
    print('==================================')
    print('Adjacent necklaces:')
    for idx in range(12):
        if chrome.is_movable(idx):
            print(f'move {idx}')
            print(chrome.move(idx))


if __name__ == '__main__':
    main()
