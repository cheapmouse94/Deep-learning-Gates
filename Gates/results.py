import matplotlib.pyplot as plt

class Plot:
    def __init__(self):
        self.x_axis = []
        self.y_axis_accurate = []
        self.y_axis_reward = []
        self.sampling = 50
        self.reward = 0

    def generate_results(self, frame, score, reward, punishmets):
        self.punishmets = punishmets
        self.frame = frame
        self.score = score
        self.reward = reward
        if self.frame % self.sampling == 0 and self.frame != 0:
            if self.score == 0 and self.punishmets == 0:
                self.accurate = 0
            else:
                self.accurate = (self.score/(self.score+self.punishmets))*100
                self.accurate = float("{:.2f}".format(self.accurate))
            self.x_axis.append(self.frame)
            self.y_axis_accurate.append(self.accurate)
            self.y_axis_reward.append(self.reward)

        if self.frame >= 1000:
            fig, axs = plt.subplots(2)
            fig.suptitle('Machine Learning final results')
            axs[0].plot(self.x_axis, self.y_axis_reward, 'tab:red')
            axs[0].set_title("Mean of the rewards")
            axs[0].set_ylabel("Rewards")
            
            axs[1].plot(self.x_axis, self.y_axis_accurate, 'tab:blue')
            axs[1].set_title("Accuration of learning")
            axs[1].set_xlabel("Iteration")
            axs[1].set_ylabel("Accuracy [%]")

            plt.show()
            print(f'Zakończono proces nauczania z wynikiem: {self.score} oraz z dokładnością nauczania: {self.accurate}')
            return False
        return True
        