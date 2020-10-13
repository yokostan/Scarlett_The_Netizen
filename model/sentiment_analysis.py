# this file is for models to perform sentiment_analysis
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score

class StochasticGradientDescent:
    def __init__(self):
        self.count_vect = CountVectorizer()

    def train(self, X_train, y_train, X_val, y_val, losses=None, learning_rates=None, tols=None, max_iter=None):
        def get_param(param, default):
            return param if param is not None else default   
        X_train = self.count_vect.fit_transform(['' if x is np.nan else x for x in X_train])
        if len(X_val) > 0: # we have val data to tune the params
            max_accuracy = 0
            current_best_model = None
            index = 0
            losses = get_param(losses,["hinge"])
            learning_rates = get_param(learning_rates,["optimal"])
            tols = get_param(tols,[1e-3])
            for loss in losses:
                for learning_rate in learning_rates:
                    for tol in tols:
                        print("Number "+str(index)+" training started")
                        model = SGDClassifier(loss=loss, learning_rate=learning_rate, penalty="l2", max_iter=get_param(max_iter,500), tol=tol)
                        model.fit(X_train, y_train)
                        y_val_pred = model.predict(self.count_vect.transform(['' if x is np.nan else x for x in X_val]))
                        accuracy = accuracy_score(y_val, y_val_pred)
                        if accuracy > max_accuracy:
                            current_best_model = model
                            max_accuracy = accuracy    
                        index += 1             
        else:
            print("training started")
            current_best_model = SGDClassifier(loss="hinge", penalty="l2", max_iter=500, tol=1e-3)
            current_best_model.fit(X_train, y_train)
            y_val_pred = current_best_model.predict(self.count_vect.transform(['' if x is np.nan else x for x in X_val]))
            max_accuracy = accuracy_score(y_val, y_val_pred)
        print('The parameters of the best model are: ')
        print(current_best_model)
        print('The validation accuracy is '+str(max_accuracy))
        return current_best_model

    def predict(self, model, X_test, y_test, filename):
        y_pred = model.predict(self.count_vect.transform(['' if x is np.nan else x for x in X_test]))
        df = pd.DataFrame ({'message': X_test,'true_label': y_test,'pred_label': y_pred})
        df.to_csv(filename+'.csv', index=False)  
        print('The prediction accuracy is '+str(accuracy_score(y_test, y_pred)))
        print('---------------------------------------------------------------------------')