import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from Classifier import *


def prepare_data(boards) -> tuple[np.array, np.array, np.array, np.array]:
    """
    Divide boards depends on contract made

    :param boards: list of all boards
    :return:
    """
    points = []
    success_3nt = []
    success_color = []
    success_both = []

    for board in boards:
        total_points = board[0][4] + board[1][4]
        if board[2][0][2] == True and ((board[2][1][2] == True or board[2][2][2] == True) or (
                board[2][3][2] == True or board[2][4][2] == True)):
            success_both.append(1)
            success_color.append(0)
            success_3nt.append(0)
        elif board[2][0][2]:
            success_both.append(0)
            success_color.append(0)
            success_3nt.append(1)
        elif (board[2][1][2] == True or board[2][2][2] == True) or (board[2][3][2] == True or board[2][4][2] == True):
            success_both.append(0)
            success_color.append(1)
            success_3nt.append(0)
        points.append(total_points)

    return np.array(points).reshape(-1, 1), np.array(success_3nt), np.array(success_color), np.array(success_both)

points_4_4, success_3nt_4_4, success_color_4_4, success_both_4_4 = prepare_data(longestSuit4_4)
points_5_4, success_3nt_5_4, success_color_5_4, success_both_5_4 = prepare_data(longestSuit5_4)
points_5_5, success_3nt_5_5, success_color_5_5, success_both_5_5 = prepare_data(longestSuit5_5)
points_6_4, success_3nt_6_4, success_color_6_4, success_both_6_4 = prepare_data(longestSuit6_4)
points_6_5, success_3nt_6_5, success_color_6_5, success_both_6_5 = prepare_data(longestSuit6_5)


def perform_regression(points, success) -> tuple[LinearRegression, PolynomialFeatures]:
    """
    :param points: np.array of points
    :param success: np.array of success (boolean)
    :return: LinearRegression, PolynomialFeatures
    """
    polynomial_features = PolynomialFeatures(degree=2)
    X_poly = polynomial_features.fit_transform(points)
    regressor = LinearRegression()
    regressor.fit(X_poly, success)
    return regressor, polynomial_features

regressor_3nt_4_4, poly_3nt_4_4 = perform_regression(points_4_4, success_3nt_4_4)
regressor_color_4_4, poly_color_4_4 = perform_regression(points_4_4, success_color_4_4)
regressor_both_4_4, poly_both_4_4 = perform_regression(points_4_4, success_both_4_4)

regressor_3nt_5_4, poly_3nt_5_4 = perform_regression(points_5_4, success_3nt_5_4)
regressor_color_5_4, poly_color_5_4 = perform_regression(points_5_4, success_color_5_4)
regressor_both_5_4, poly_both_5_4 = perform_regression(points_5_4, success_both_5_4)

regressor_3nt_5_5, poly_3nt_5_5 = perform_regression(points_5_5, success_3nt_5_5)
regressor_color_5_5, poly_color_5_5 = perform_regression(points_5_5, success_color_5_5)
regressor_both_5_5, poly_both_5_5 = perform_regression(points_5_5, success_both_5_5)

regressor_3nt_6_4, poly_3nt_6_4 = perform_regression(points_6_4, success_3nt_6_4)
regressor_color_6_4, poly_color_6_4 = perform_regression(points_6_4, success_color_6_4)
regressor_both_6_4, poly_both_6_4 = perform_regression(points_6_4, success_both_6_4)

regressor_3nt_6_5, poly_3nt_6_5 = perform_regression(points_6_5, success_3nt_6_5)
regressor_color_6_5, poly_color_6_5 = perform_regression(points_6_5, success_color_6_5)
regressor_both_6_5, poly_both_6_5 = perform_regression(points_6_5, success_both_6_5)


def plot_regression(points, success_3nt, success_color, success_both, regressor_3nt, poly_3nt, regressor_color,
                    poly_color, regressor_both, poly_both, title):
    """
    :param points: np.array of points
    :param success_3nt: np.array of success of 3NT (boolean)
    :param success_color: np.array of success of color game (boolean)
    :param success_both: np.array of success of both games (boolean)
    :param regressor_3nt: LinearRegression for 3NT
    :param poly_3nt: PolynomialFeatures for 3NT
    :param regressor_color: LinearRegression for color game
    :param poly_color: PolynomialFeatures for color game
    :param regressor_both: LinearRegression for both games
    :param poly_both: PolynomialFeatures for both games
    :param title: plot title
    """
    X_range = np.linspace(min(points), max(points), 100).reshape(-1, 1)

    X_poly_range_3nt = poly_3nt.transform(X_range)
    y_pred_3nt = regressor_3nt.predict(X_poly_range_3nt)

    X_poly_range_color = poly_color.transform(X_range)
    y_pred_color = regressor_color.predict(X_poly_range_color)

    X_poly_range_both = poly_both.transform(X_range)
    y_pred_both = regressor_both.predict(X_poly_range_both)

    plt.scatter(points, success_3nt, color='red', label='Tylko 3NT', alpha=0.5)
    plt.scatter(points, success_color, color='green', label='Tylko kolor', alpha=0.5)
    plt.scatter(points, success_both, color='blue', label='Oba', alpha=0.5)

    plt.plot(X_range, y_pred_3nt, color='red')
    plt.plot(X_range, y_pred_color, color='green')
    plt.plot(X_range, y_pred_both, color='blue')

    plt.xlabel('Liczba punktów')
    plt.ylabel('Prawdopodobieństwo wygrania kontraktu')
    plt.title(title)
    plt.legend(loc='upper right')
    plt.grid(True)


plt.figure(figsize=(16, 8))

plt.subplot(151)
plot_regression(points_4_4, success_3nt_4_4, success_color_4_4, success_both_4_4,
                regressor_3nt_4_4, poly_3nt_4_4,
                regressor_color_4_4, poly_color_4_4,
                regressor_both_4_4, poly_both_4_4, 'Najdłuższy kolor 4 do 4')

plt.subplot(152)
plot_regression(points_5_4, success_3nt_5_4, success_color_5_4, success_both_5_4,
                regressor_3nt_5_4, poly_3nt_5_4,
                regressor_color_5_4, poly_color_5_4,
                regressor_both_5_4, poly_both_5_4, 'Najdłuższy kolor 5 do 4')

plt.subplot(153)
plot_regression(points_5_5, success_3nt_5_5, success_color_5_5, success_both_5_5,
                regressor_3nt_5_5, poly_3nt_5_5,
                regressor_color_5_5, poly_color_5_5,
                regressor_both_5_5, poly_both_5_5, 'Najdłuższy kolor 5 do 5')

plt.subplot(154)
plot_regression(points_6_4, success_3nt_6_4, success_color_6_4, success_both_6_4,
                regressor_3nt_6_4, poly_3nt_6_4,
                regressor_color_6_4, poly_color_6_4,
                regressor_both_6_4, poly_both_6_4, 'Najdłuższy kolor 6 do 4')

plt.subplot(155)
plot_regression(points_6_5, success_3nt_6_5, success_color_6_5, success_both_6_5,
                regressor_3nt_6_5, poly_3nt_6_5,
                regressor_color_6_5, poly_color_6_5,
                regressor_both_6_5, poly_both_6_5, 'Najdłuższy kolor 6 do 5')

plt.tight_layout()
plt.show()
