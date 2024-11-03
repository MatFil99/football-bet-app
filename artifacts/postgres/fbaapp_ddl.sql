
create table fbaapp.users (
user_id			smallint GENERATED ALWAYS AS IDENTITY,
firstname		varchar(30),
surname			varchar(30),
pass_hash		varchar(100),
username		varchar(20),
email			varchar(100),
CONSTRAINT PK_USERS PRIMARY KEY (user_id)
);


create table fbaapp.football_teams ( 
football_team_id	smallint,
name				varchar(30),
CONSTRAINT FOOTBALL_TEAMS_PK PRIMARY KEY (football_team_id)
);

create table fbaapp.matches (
match_id			int4,
home_team_id		smallint,
away_team_id		smallint,
matchday			smallint,
date				timestamp,
season				varchar(9), -- example: '2024/2025'
home_score			smallint,
away_score			smallint,
CONSTRAINT MATCHES_PK PRIMARY KEY (match_id),
CONSTRAINT HOME_TEAMS_FK FOREIGN KEY (home_team_id) REFERENCES fbaapp.football_teams(football_team_id),
CONSTRAINT AWAY_TEAMS_FK FOREIGN KEY (away_team_id) REFERENCES fbaapp.football_teams(football_team_id)
);

create table fbaapp.match_predictions (
match_id			int4,
user_id			smallint,
home_score_pred		smallint,
away_score_pred		smallint,
points				smallint,
CONSTRAINT MATCH_PREDICTIONS_PK PRIMARY KEY (match_id,user_id),
CONSTRAINT USERS_FK FOREIGN KEY (user_id) REFERENCES fbaapp.users(user_id),
CONSTRAINT MATCHES_FK FOREIGN KEY (match_id) REFERENCES fbaapp.matches(match_id)
);


