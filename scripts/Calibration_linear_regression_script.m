% Define sample data
x = [1602.22 1683.52 1768.30 1850.24 1934.02 2015.75 2085.32 2187.42 2269.39 2352.40 2430.85];
y = [-5 -4 -3 -2 -1 0 1 2 3 4 5];

% Perform linear regression
coefficients = polyfit(x, y, 1);  % Fit a first-degree (linear) polynomial
slope = coefficients(1);
intercept = coefficients(2);

% Compute predicted y values
y_predicted = polyval(coefficients, x);

% Calculate residuals
residuals = y - y_predicted;

% Calculate total sum of squares
total_sum_of_squares = sum((y - mean(y)).^2);

% Calculate residual sum of squares
residual_sum_of_squares = sum(residuals.^2);

% Calculate R-squared
r_squared = 1 - (residual_sum_of_squares / total_sum_of_squares);

% Display the R-squared value
disp(['R-squared (coefficient of determination): ', num2str(r_squared)]);

% Display the results
disp(['Slope (m): ', num2str(slope)]);
disp(['Intercept (b): ', num2str(intercept)]);

x_fit = min(x):0.1:max(x);  % Generate x values for regression line
y_fit = polyval(coefficients, x_fit);  % Compute y values for regression line

% Plot the data and regression line
plot(x_fit, y_fit, 'LineWidth', 2);  % Plot regression line
hold on;

% Plot the data
plot(x, y, '.', 'MarkerSize', 14);  % Plot data points
hold on;

set(gca, "TickLabelInterpreter", "latex");
set(gca, "fontsize", 14);
xlabel("Valor do ADC", "Interpreter", "latex", "fontsize", 14);
ylabel("Tens\~ao de entrada [V]", "Interpreter", "latex", "fontsize", 14);
legend(sprintf('$y = 0.012021x - 24.238022$ \n $r^2 = 0.999664$'), 'Interpreter', 'latex', 'Location','northwest');
xlim([1500 2500]);
xticks(1500:250:2500)
ylim([-5 5]);
yticks(-5:1:5);
grid on;
