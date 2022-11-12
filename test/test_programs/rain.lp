% Program Reading
% WA 1: <{cloudy},{cloudy}>,
%       <{rainy, prepare_rain_gear},{rainy, prepare_rain_gear}>
% WA 2: <{cloudy, prepare_rain_gear},{cloudy, prepare_rain_gear}>,
%       <{rainy, prepare_rain_gear},{rainy, prepare_rain_gear}>

:- &c{rainy}, not prepare_rain_gear.
in_plum_rain_season.
rainy | cloudy :- in_plum_rain_season.
prepare_rain_gear :- &c{rainy}.

#show rainy/0.
#show cloudy/0.
#show prepare_rain_gear/0.