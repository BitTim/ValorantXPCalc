import 'package:vextrack/Models/History/history_entry.dart';
import 'package:vextrack/Models/History/history_entry_group.dart';

class HistoryCalc
{
  static List<HistoryEntryGroup> groupHistoryByDate(List<HistoryEntry> history) {
    List<HistoryEntryGroup> groupedHistory = [];

    for (HistoryEntry he in history)
    {
      if (groupedHistory.isEmpty)
      {
        groupedHistory.add(HistoryEntryGroup(he.getDate(), [he]));
      }
      else
      {
        if (groupedHistory.last.date == he.getDate()) {
          groupedHistory.last.entries.add(he);
        } else {
          groupedHistory.add(HistoryEntryGroup(he.getDate(), [he]));
        }
      }
    }

    return groupedHistory;
  }

  static Map<String, dynamic> getExtremeDays(List<HistoryEntry> history)
  {
    DateTime prevDate = history[0].getDate();
    int dayTotal = 0;

    DateTime strongestDate = prevDate;
    int strongestXP = 0;

    DateTime weakestDate = prevDate;
    int weakestXP = 0;

    for (HistoryEntry he in history)
    {
      if (he.getDate() == prevDate)
      {
        dayTotal += he.xp;
      }
      else
      {
        if (dayTotal > strongestXP)
        {
          strongestXP = dayTotal;
          strongestDate = prevDate;
        }

        if (dayTotal < weakestXP || weakestXP == 0)
        {
          weakestXP = dayTotal;
          weakestDate = prevDate;
        }

        prevDate = he.getDate();
        dayTotal = he.xp;
      }
    }

    return {
      "strongestDate": strongestDate,
      "strongestXP": strongestXP,
      "weakestDate": weakestDate,
      "weakestXP": weakestXP,
    };
  }
}