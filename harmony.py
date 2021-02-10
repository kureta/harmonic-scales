def interval_to_binary(necklace):
    return sum([[1] + (n - 1) * [0] for n in necklace], [])


def binary_to_interval(neckalce):
    intervals = []
    current_interval = 0
    for item in neckalce:
        if item == 1:
            if current_interval == 0:
                current_interval = 1
            else:
                intervals.append(current_interval)
                current_interval = 1
        elif item == 0:
            current_interval += 1
        else:
            raise ValueError
    intervals.append(current_interval)
    return BinaryNecklace(intervals)


class BinaryNecklace(tuple):
    @classmethod
    def from_intervals(cls, intervals):
        return cls(interval_to_binary(intervals))  # noqa

    def __eq__(self, other):
        for idx in range(len(self)):
            if tuple.__eq__(self[idx:] + self[:idx], other):
                return True
        return False

    @property
    def intervals(self):
        return binary_to_interval(self)

    @property
    def is_harmonic(self):
        thirds = [3, 4]
        for first, second in zip(self.intervals, self.intervals[1:] + self.intervals[:1]):
            third = first + second
            if third not in thirds:
                return False
        return True


major = BinaryNecklace([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
melodic_minor = BinaryNecklace([1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1])
harmonic_minor = BinaryNecklace([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1])
#                               [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1]
harmonic_major = BinaryNecklace([1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1])
whole_tone = BinaryNecklace([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])  # has only 2 colors (transpositions)
octatonic = BinaryNecklace([1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1])  # 3 colors
augmented = BinaryNecklace([1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0])  # 4 colors

# All proper scales have 12 colors
proper_scales = [major, melodic_minor, harmonic_major, harmonic_minor]
improper_scales = [whole_tone, octatonic, augmented]
all_scales = proper_scales + improper_scales


# For now, we will ignore improper scales. Our objects have a shape and a color. Scale families represent shapes.
# Base pitch of the scale represent color (index of its first tone, or its rotation, transposition).
class ChromaticNecklace:
    def __init__(self, shape: BinaryNecklace, color: int):
        if color not in range(12):
            raise ValueError
        self.shape = shape
        self.color = color


def main():
    for s in proper_scales:
        print(harmonic_major.all_distances(s))


if __name__ == '__main__':
    main()
