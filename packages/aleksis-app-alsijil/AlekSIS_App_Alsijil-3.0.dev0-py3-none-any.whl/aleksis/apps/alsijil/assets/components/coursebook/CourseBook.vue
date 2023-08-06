<template>
  <ApolloQuery
    :query="require('./CourseBook.graphql')"
    :variables="{ lessonId: $route.params.lessonId }"
  >
    <template v-slot="{ result: { loading, error, data } }">
        <!-- Error -->
        <message-box v-if="error" type="error">An error occurred</message-box>
    
        <!-- Result -->
        <div v-else-if="data" class="result apollo">
          <div class="d-flex justify-space-between">
            <v-btn text color="primary" :href="$root.urls.select_coursebook()">
              <v-icon left>mdi-chevron-left</v-icon>
              {{ $root.django.gettext("Back") }}
            </v-btn>
            <update-indicator @manual-update="updateManually()" ref="indicator" :status="status"></update-indicator>
          </div>
          <v-row>
            <v-col cols="12">
              <lesson-documentations
                :lesson-documentations="data.lessonDocumentations"
                :planned-lesson-periods-date-times="data.lesson.plannedLessonperiodsDatetimes"
                :groups="data.lesson.groups"
                :excuse-types="data.excuseTypes"
                :extra-marks="data.extraMarks"
                :save-lesson-documentations-per-week="saveLessonDocumentationsPerWeek"
              />
            </v-col>
          </v-row>
        </div>
        <!-- No result or Loading -->
        <div v-else class="text-center">
          <v-progress-circular
            indeterminate
            color="primary"
            class="ma-auto"
          ></v-progress-circular>
        </div>
    </template>
  </ApolloQuery>
</template>

<script>
import {CHANGES, SAVED, UPDATING} from "../../UpdateStatuses.js";
import UpdateIndicator from "./UpdateIndicator.vue";
import LessonDocumentations from "./LessonDocumentations.vue";

export default {
    components: {
        UpdateIndicator,
        LessonDocumentations,
    },
    props: [ "saveLessonDocumentationsPerWeek" ],
    methods: {
        processDataChange(event) {
            this.status = CHANGES;
            // alert("Probably save the data");
            console.log(event);
            setTimeout(() => {
                this.status = UPDATING;
            }, 500)

            setTimeout(() => {
                this.status = SAVED;
            }, 1000)

        },
        updateManually(event) {
            alert("Data sync triggered manually");
            this.status = UPDATING;
            setTimeout(() => {
                this.status = SAVED;
            }, 500)
        },
    },
    name: "course-book",
    data: () => {
        return {
            ping: "ping",
            status: SAVED,
        }
    }
}
</script>
