major = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
melodic_minor = [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
harmonic_minor = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
harmonic_major = [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1]
whole_tone = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # has only 2 colors (transpositions)
octatonic = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1]  # 3 colors
augmented = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]  # 4 colors

# All proper scales have 12 colors
proper_scales = [major, melodic_minor, harmonic_major, harmonic_minor]
improper_scales = [whole_tone, octatonic, augmented]
all_scales = proper_scales + improper_scales


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
        swapped = self.state.copy()
        swapped[idx], swapped[(idx + 1) % len(swapped)] = 0, 1
        return swapped

    def movable(self, idx):
        if not (self.state[idx] == 1 and self.state[(idx + 1) % len(self.state)] == 0):
            return False
        swapped = self.sharpened_state(idx)
        return BinaryNecklace(swapped).is_harmonic

    def move(self, idx):
        if not self.movable(idx):
            raise ValueError
        swapped = self.sharpened_state(idx)
        swapped = BinaryNecklace(swapped)
        for name, shape in scales.items():
            if swapped == shape:
                new_shape, new_color = name, get_transposition(tuple(swapped), tuple(shape))
                return ChromaticNecklace(new_shape, new_color)


def main():
    chrome = ChromaticNecklace('major', 0)
    print('Initial necklace:')
    print(chrome)
    print('==================================')
    print('Adjacent necklaces:')
    for idx in range(12):
        if chrome.movable(idx):
            print(f'move {idx}')
            print(chrome.move(idx))


if __name__ == '__main__':
    main()
