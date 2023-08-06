<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        right
        icon

        v-bind="attrs"
        v-on="on"

        @click="() => {isAbleToClick ? $emit('manual-update') : null}"
        :loading="status === UPDATING"
      >
        <v-icon
          v-if="status !== UPDATING"
          :color="color"
        >
          {{ icon }}
        </v-icon>
      </v-btn>
    </template>
    <span>{{ text }}</span>
  </v-tooltip>
</template>

<script>
import {CHANGES, ERROR, SAVED, UPDATING} from "../../UpdateStatuses.js";

export default {
    created() {
        this.ERROR = ERROR;
        this.SAVED = SAVED;
        this.UPDATING = UPDATING;
        this.CHANGES = CHANGES;
    },
    name: "update-indicator",
    emits: ["manual-update"],
    props: ["status"],
    computed: {
        text() {
            switch (this.status) {
                case SAVED:
                    return this.$root.django.gettext("All changes are processed.");
                case UPDATING:
                    return this.$root.django.gettext("Changes are being synced.");
                case CHANGES:
                    return this.$root.django.gettext("You have unsaved changes. Click to save immediately.");
                default:
                    return this.$root.django.gettext("There has been an error processing the latest changes.");
            }
        },
        color() {
            switch (this.status) {
                case SAVED:
                    return "success";
                case CHANGES:
                    return "secondary";
                case UPDATING:
                    return "secondary";
                default:
                    return "error";
            }
        },
        icon() {
            // FIXME use app sdhasdhahsdhsadhsadh
            switch (this.status) {
                case SAVED:
                    return "mdi-check-circle-outline";
                case CHANGES:
                    return "mdi-dots-horizontal";
                default:
                    return "mdi-alert-outline";
            }
        },
        isAbleToClick() {
            return this.status === CHANGES || this.status === ERROR;
        }
    },
}
</script>
