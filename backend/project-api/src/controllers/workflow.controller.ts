import { Request, Response, NextFunction } from 'express';
import { callNeuralApiStage1, callNeuralApiStage2, callNeuralApiReview } from '../services/neuralApi.service';
import { internalAlgorithm } from '../services/internalAlgo.service';
import { getAllTeams } from '../services/developer.service';

export const processData = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const input = req.body;
    const developers = await getAllTeams();

    // Первый этап: весь список команд
    const merged = {
      today: new Date().toISOString(),
      ...input,
      developers,
    };

    const tasksRaw = await callNeuralApiStage1(JSON.stringify(merged));
    const tasksContent = tasksRaw.choices?.[0]?.message?.content;
    const tasks = tasksContent ? JSON.parse(tasksContent) : null;

    // ---- Вот тут находим команду по выбранному id ----
    const chosen_team_id = tasks.chosen_team_id;

    // developers -- это массив объектов { "0": [...], "1": [...], ... }
    // поэтому надо найти объект с нужным ключом-строкой
    // или преобразовать developers в мапу для быстроты
    const chosenTeamObj = developers.find((team: any) => team[chosen_team_id]);
    const chosenTeam = chosenTeamObj ? chosenTeamObj[chosen_team_id] : [];

    const merged2 = {
      today: new Date().toISOString(),
      ...tasks,
      developers: chosenTeam,   // !!! тут только выбранная команда !!!
    };
    // res.status(200).json({
    //   merged2
    // });

    // return
    const spendingRaw = await callNeuralApiStage2(JSON.stringify(merged2));
    const spendingContent = spendingRaw.choices?.[0]?.message?.content;
    const spending = spendingContent ? JSON.parse(spendingContent) : null;

    res.status(200).json({
      tasks,
      spending,
    });
  } catch (err) {
    next(err);
  }
};