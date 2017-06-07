# IPython log file


T = pd.read_csv('bundoora-temp.csv')
T.head()
T.rename(columns={'Mean maximum temperature (°C)':'Temperature'},
         inplace=True)
         
T['Date'] = T['Year'] + (T['Month'] - 0.5) / 12
dates = T['Date']
temps = T['Temperature']
def predicted_temperature(parameters, time):
    t0, w, A, omega, phi = parameters
    return t0 + w*time + A * np.sin(omega*time + phi)
def prediction_error(parameters, time, true_temperature):
    return true_temperature - predicted_temperature(parameters, time)
def predicted_temperature_null(parameters, time):
    t0, w, A, omega, phi = parameters
    return t0 + A * np.sin(omega*time + phi)
t0 = np.mean(temps)
w = 0
A = np.max(temps) - np.min(temps)
omega = np.pi * 2
phi = np.pi / 2

params0 = [t0, w, A, omega, phi]
params, success = optimize.leastsq(prediction_error, params0,
                                   args=(dates, temps))
                                   
from scipy import optimize
params, success = optimize.leastsq(prediction_error, params0,
                                   args=(dates, temps))
                                   
success
def prediction_error_null(parameters, time, true_temperature):
    return true_temperature - predicted_temperature_null(parameters, time)

paramsnull, successnull = optimize.leastsq(prediction_error_null,
                                           params0,
                                           args=(dates, temps))
                                           
successnull
from scipy import stats
predicted = predicted_temperature(params, dates)
predicted_null = predicted_temperature_null(params, dates)
chisq1 = (temps - predicted)**2 / predicted
chisq0 = (temps - predicted_null)**2 / predicted_null
chisqdiff = chisq1 - chisq0
chisqdiff
chisq1 = np.sum((temps - predicted)**2 / predicted)
chisq0 = np.sum((temps - predicted_null)**2 / predicted_null)
chisqdiff = chisq1 - chisq0
chisqdiff
chisq_dof = len(temps)
chisq_dof
chisq1
chisq2
chisq0
plt.plot(dates, predicted_null)
import statsmodels
from statsmodels import stats
np.mean((temps - predicted)**2)
plt.plot(dates, predicted)
params
plt.plot(dates, temps)
def predicted_temperature_null(parameters, time):
    t0, A, omega, phi = parameters
    return t0 + A * np.sin(omega*time + phi)
def prediction_error_null(parameters, time, true_temperature):
    return true_temperature - predicted_temperature_null(parameters, time)

paramsnull, successnull = optimize.leastsq(prediction_error_null,
                                           [params0[0]] + params0[2:],
                                           args=(dates, temps))
                                           
successnull
predicted_null = predicted_temperature_null(paramsnull, dates)
plt.plot(dates, temps)
plt.plot(dates, predicted_null)
np.mean((temps - predicted_null)**2)
np.mean((temps - predicted)**2)
ssdiff = 401 * (_48 - _49)
ssdiff
from scipy import stats
stats.gamma
stats.chi2
get_ipython().magic('pinfo stats.chisquare')
get_ipython().set_next_input('c2 = stats.chi2');get_ipython().magic('pinfo stats.chi2')
c2 = stats.chi2.sf(ssdiff, 401)
c2
c2 = stats.chi2.sf(ssdiff, 4)
c2
