import 'package:uuid/uuid.dart';
import 'package:vextrack/Core/history_calc.dart';
import 'package:vextrack/Models/Contracts/contract.dart';
import 'package:vextrack/Models/Contracts/goal.dart';
import 'package:vextrack/Models/Seasons/season.dart';
import 'package:vextrack/Models/Seasons/season_meta.dart';
import 'package:vextrack/Services/data.dart';

class DailyContract extends Contract
{
  DailyContract(super.id, super.name, super.timed, super.paused, super.startColor, super.endColor, super.startTime, super.endTime);
  
  static DailyContract empty()
  {
    return DailyContract(
      const Uuid().v4(),
      "Daily Contract",
      false,
      false,
      "",
      "",
      null,
      null,
    );
  }

  static Future<DailyContract> init(String uid) async
  {
    DailyContract dc = DailyContract.empty();

    SeasonMeta? meta = await DataService.getActiveSeasonMeta();
    if (meta == null) return dc;

    Season season = await DataService.getSeason(uid, meta.id);
    
    int dayIndex = season.getDaysIndexFromDate(DateTime.now());
    int dailyTotal = season.getUserIdeal();
    int dailyEpilogueTotal = season.getUserEpilogueIdeal() - dailyTotal;
    int dailyXP = HistoryCalc.getXPPerDay(season.history, meta)[dayIndex];

    dc.goals.add(Goal(
      dc,
      const Uuid().v4(),
      "Battlepass",
      dailyTotal,
      0,
      0,
      []
    ));

    dc.goals.add(Goal(
      dc,
      const Uuid().v4(),
      "Epilogue",
      dailyEpilogueTotal,
      0,
      0,
      []
    ));
    
    dc.addXP(dailyXP);
    return dc;
  }



  double getMaxProgress()
  {
    if(goals.length < 2) return 0;

    double total = goals[0].getTotal().toDouble();
    double totalEpilogue = goals[1].getTotal().toDouble();
    return (total + totalEpilogue) / total;
  }




  bool hasCompleted() {
    if(goals.length < 2) return false;
    if(goals[0].getProgress() >= 1) return true;
    return false;
  }

  bool hasEpilogue() {
    if(goals.length < 2) return false;
    if(goals[1].getProgress() >= 1) return true;
    return false;
  }
}