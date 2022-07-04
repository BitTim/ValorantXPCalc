import 'package:flutter/cupertino.dart';
import 'package:vextrack/Components/history_entry.dart';
import 'package:vextrack/Constants/colors.dart';
import 'package:vextrack/Models/history_entry_group.dart';

class HistoryEntryGroupWidget extends StatefulWidget
{
  final HistoryEntryGroup model;
  const HistoryEntryGroupWidget({Key? key, required this.model}) : super(key: key);
  
  @override
  HistoryEntryGroupWidgetState createState() => HistoryEntryGroupWidgetState();
}

class HistoryEntryGroupWidgetState extends State<HistoryEntryGroupWidget>
{
  @override
  Widget build(BuildContext context)
  {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0, 0, 0, 8),
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(0, 8, 0, 8),
            child: Text(
              widget.model.getFormattedDate(),
              style: const TextStyle(
                color: AppColors.lightTextSecondary,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          ...widget.model.entries.map((entry) => HistoryEntryWidget(model: entry)),
        ],
      ),
    );
  }
}