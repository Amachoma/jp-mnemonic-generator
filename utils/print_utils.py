def draw_progress_bar(progress):
    bar_length = 50
    completed_length = int(bar_length * progress)
    bar = '█' * completed_length + '-' * (bar_length - completed_length)

    percentage = progress * 100
    print(f'[{bar}] {percentage:.2f}% complete')