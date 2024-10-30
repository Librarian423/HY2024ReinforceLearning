import matplotlib.pyplot as plt

plt.ion()  # 인터랙티브 모드 활성화

def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label="Score")
    plt.plot(mean_scores, label="Mean Score")
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]), fontsize=12)
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]), fontsize=12)
    plt.legend()
    plt.draw()   # 그래프를 그리기
    plt.pause(0.1)
