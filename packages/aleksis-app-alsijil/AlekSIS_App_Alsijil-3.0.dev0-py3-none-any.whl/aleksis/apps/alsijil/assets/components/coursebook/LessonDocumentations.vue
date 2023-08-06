<template><div>
  <v-dialog
    v-model="dialog"
    max-width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-row>
        <v-col cols="12" md="6" class="pb-0 pb-md-3">
          <v-select
            v-if="saveLessonDocumentationsPerWeek === 'True'"
            :items="emptyLessonPeriods"
            label="Choose week"
            :item-text="getWeekText"
            item-value="datetimeStart"
            v-model="selectedLessonPeriodDatetime"
          ></v-select>
          <v-select
            v-else
            :items="emptyLessonPeriods"
            label="Choose Lesson date"
            :item-text="getLessonText"
            v-model="selectedLessonPeriodDatetime"
            return-object
          ></v-select>
        </v-col>
        <v-col cols="12" md="6" class="pt-0 pt-md-3">
          <v-btn
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
            @click="createLessonDocumentation()"
          >
            {{ $root.django.gettext("Create documentation") }}
          </v-btn>
        </v-col>
      </v-row>
    </template>
    <lesson-documentation
      :lesson-documentation-edit="lessonDocumentationEdit"
      :groups="groups"
      :excuse-types="excuseTypes"
      :extra-marks="extraMarks"
      :save-lesson-documentations-per-week="saveLessonDocumentationsPerWeek"
      :get-week-text="getWeekText"
      @cancel-lesson-documentation-dialog="cancelDialog"
    />
  </v-dialog>
  <v-data-table
    :headers="headers"
    :items="computedLessonDocumentations"
    @click:row="editLessonDocumentation"
    class="elevation-1 my-3"
    :expanded.sync="expanded"
    show-expand
    multi-sort
    :sort-by="['year','week']"
    :sort-desc="[true, true]"
  >
    <template v-slot:item.period="{ item }">
      <span class="text-no-wrap">{{ (saveLessonDocumentationsPerWeek === "True") ? getWeekText(item) : getLessonText(item) }}</span>
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <template v-if="saveLessonDocumentationsPerWeek === 'True'" v-for="lessonDocumentation in item.documentations">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>{{ getLessonText(lessonDocumentation) }}</v-list-item-title>
              <v-list-item-action>
                <personal-notes
                    :lesson-documentation-id="lessonDocumentation.id"
                    :groups="groups"
                    :excuse-types="excuseTypes"
                    :extra-marks="extraMarks"

                    v-model="lessonDocumentation.personalNotes"
                    @change="$emit('change-personal-notes', $event)"
                ></personal-notes>
              </v-list-item-action>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
        </template>
        <template v-else v-for="personalNote in item.personalNotes">
<!--          FIXME: Add edit and delete functionality to personal note chips-->
          <v-chip class="ma-1" v-if="personalNoteString(personalNote)">
            {{ personalNote.person.fullName }}: {{ personalNoteString(personalNote) }}
          </v-chip>
        </template>
      </td>
    </template>
</v-data-table>
</div></template>

<script>
  import LessonDocumentation from "./LessonDocumentation.vue";
  import PersonalNotes from "./PersonalNotes.vue";
  export default {
    components: {LessonDocumentation, PersonalNotes},
    props: [ "lessonDocumentations", "plannedLessonPeriodsDateTimes",  "groups", "excuseTypes", "extraMarks", "saveLessonDocumentationsPerWeek" ],
    name: "lesson-documentations",
    data () {
      return {
        dialog: false,
        expanded: [],
        headers: [
          { text: "Period", value: "period" },
          { text: "Topic", value: "topic" },
          { text: "Homework", value: "homework" },
          { text: "Group note", value: "groupNote" },
          { text: "Personal notes", value: "data-table-expand" }
        ],
        lessonDocumentationEdit: {},
        selectedLessonPeriodDatetime: {},
        recordedWeeks: [],
      }
    },
    computed: {
      emptyLessonPeriods() {
        if (this.saveLessonDocumentationsPerWeek === "True") {
          let currentDatetime = new Date()
          let weeks = {}
          let lpdts = this.plannedLessonPeriodsDateTimes.filter(lp => new Date(lp.datetimeStart) > currentDatetime)
          for (let ldIndex in lpdts) {
            let ld = lpdts[ldIndex]
            if (ld.week in weeks) {
              weeks[ld.week]["planned"].push(ld)
            } else {
              weeks[ld.week] = {
                "year": ld.year,
                "week": ld.week,
                "startDate": this.calculateStartDateOfCW(ld.year, ld.week),
                "datetimeStart": ld.datetimeStart,
                "lessonPeriod": ld.lessonPeriod,
                "planned": [ld]
              }
            }
          }
          return Object.values(weeks) // FIXME sort by date
        } else {
          let currentDatetime = new Date()
          return this.plannedLessonPeriodsDateTimes.filter(lp => new Date(lp.datetimeStart) > currentDatetime)
        }
      },
      computedLessonDocumentations() {
        if (this.saveLessonDocumentationsPerWeek === "True") {
          let weeks = {}
          for (let ldIndex in this.lessonDocumentations) {
            let ld = this.lessonDocumentations[ldIndex]
            if (ld.week in weeks) {
              weeks[ld.week]["documentations"].push(ld)
            } else {
              weeks[ld.week] = {
                "id": ld.id,
                "startDate": this.calculateStartDateOfCW(ld.year, ld.week),
                "year": ld.year,
                "week": ld.week,
                "topic": ld.topic,
                "homework": ld.homework,
                "groupNote": ld.groupNote,
                "documentations": [ld]
              }
            }
          }
          return Object.values(weeks)
        } else {
          return this.lessonDocumentations
        }
      }
    },
    methods: {
      cancelDialog() {
        this.dialog = false;
        this.lessonDocumentationEdit = {};
      },
      recordDocumentation(item) {
        if (this.recordedWeeks.includes(item.week)) {
          return false
        }
        this.recordedWeeks.push(item.week)
        return true
      },
      async loadLessonDocumentation(item) {
        const result = await this.$apollo.mutate({
          mutation: require("./LessonDocumentation.graphql"),
          variables: {
            year: item.year,
            week: item.week,
            lessonPeriodId: item.lessonPeriod ? item.lessonPeriod.id : null,
            eventId: item.event ? item.event.id : null,
            extraLessonId: item.extraLesson ? item.extraLesson.id : null,
          },
        })
        let lessonDocumentation = result.data.updateOrCreateLessonDocumentation.lessonDocumentation
        this.lessonDocumentationEdit = {
          id: lessonDocumentation.id,
          year: item.year,
          week: item.week,
          date: lessonDocumentation.date,
          period: item.period,
          lessonPeriodId: item.lessonPeriod ? item.lessonPeriod.id : null,
          eventId: item.event ? item.event.id : null,
          extraLessonId: item.extraLesson ? item.extraLesson.id : null,
          topic: lessonDocumentation.topic,
          homework: lessonDocumentation.homework,
          groupNote: lessonDocumentation.groupNote,
          personalNotes: lessonDocumentation.personalNotes,
        }
      },

      editLessonDocumentation(item) {
        if (this.saveLessonDocumentationsPerWeek === "True") {
          this.loadLessonDocumentation(item.documentations[0])
        } else {
          this.loadLessonDocumentation(item)
        }
        this.dialog = true
      },

      createLessonDocumentation() { // FIXME: Update cache to show newly created LessonDocumentation in table
        let lessonDocumentation = this.selectedLessonPeriodDatetime
        lessonDocumentation["event"] = null
        lessonDocumentation["extraLesson"] = null
        this.loadLessonDocumentation(lessonDocumentation)
        this.dialog = true
      },

      calculateStartDateOfCW(year, week){
        let ld_date = new Date(Date.UTC(year, 0, 1 + (week - 1) * 7));
        let dow = ld_date.getDay();
        let start_date = ld_date;
        if (dow <= 4)
          return start_date.setDate(ld_date.getDate() - ld_date.getDay() + 1)
        else
          return start_date.setDate(ld_date.getDate() + 8 - ld_date.getDay())
      },

      getLessonText(item) {
        let date_obj = new Date(item.hasOwnProperty("datetimeStart") ? item.datetimeStart : item.date)
        let period = item.lessonPeriod ? ", " + this.$root.django.gettext('period') + " " + item.lessonPeriod.period.period : "" // FIXME: Cases without lessonPeriod
        return date_obj.toLocaleDateString(this.$root.languageCode) + period
      },
      getWeekText(item) {
        if (item.hasOwnProperty("startDate")) {
          var start_date = new Date(item.startDate)
        } else {
          let lesson_date = new Date(item.date)
          var start_date = new Date(((lesson_date.getDay() || 7) !== 1) ? lesson_date.setHours(-24 * (lesson_date.getDay() - 1)) : lesson_date)
        }
        let end_date = new Date(start_date)
        end_date.setDate(end_date.getDate() + 7)
        return start_date.toLocaleDateString(this.$root.languageCode) + " - " + end_date.toLocaleDateString(this.$root.languageCode) + ", " + this.$root.django.gettext('CW') + " " + item.week
      },
      personalNoteString(personalNote) {
          let personalNoteString = "";
          if (personalNote.late > 0) {
              personalNoteString += personalNote.late + " min. ";
          }
          if (personalNote.absent) {
              personalNoteString += this.$root.django.gettext("abwesend") + " ";
          }
          if (personalNote.excused) {
              personalNoteString += this.$root.django.gettext("entschuldigt") + " ";
          }
          if (personalNote.excuseType) {
              personalNoteString += personalNote.excuseType.name;
          }
          if (personalNote.extraMarks.length > 0) {
              personalNoteString += " (";
              personalNote.extraMarks.forEach(item => {
                  personalNoteString += item.name + ", ";
              });
              personalNoteString = personalNoteString.substring(0, personalNoteString.length - 2);
              personalNoteString += ") ";
          }
          if (personalNote.remarks) {
              personalNoteString += "\"" + personalNote.remarks + "\" ";
          }
          return personalNoteString;
      },
    }
  }
</script>
